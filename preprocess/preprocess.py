import os
import sys
from time import sleep
import requests
import signal


path = '/'.join(os.getcwd().split('/')[:-1]) + '/'
sys.path.insert(0, path)

from database.request_queue_db import select_min_request
from database.request_queue_db import update_submit
from database.request_queue_db import delete_row
from database.request_submited_queue_db import add_row
import database.database_manager as db_manager


def connect(headers: dict, data: str) -> tuple:
    try:
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=data)
        return True, response
    except:
        return False, ''


def post_to_url_scan(api_key: str, url: str) -> tuple:
    headers = {
        'Content-Type': 'application/json',
        'API-Key': api_key,
    }
    data = '{"url": "' + url + '", "public": "on"}'

    lives = 5
    uuid = ''
    while True:
        succ_connection, response = connect(headers, data)
        print(response)
        print(response.text)
        if succ_connection:
            try:
                res_dict = dict(response.json())
                if 'Submission successful' in res_dict['message']:
                    print('Submission successful')
                    uuid = res_dict['uuid']
                    break
                elif 'be silly now ...' in res_dict['message']:
                    """
                    Not valid url.
                    """
                    return False, ''
            except:
                print('sleeing in post 1 ')
                # sleep_time = random.uniform(0, 2) + 3
                sleep_time = 2
                sleep(sleep_time)
                lives += -1
        else:
            print('sleeing in post 2')
            lives += -1
            # sleep_time = random.uniform(0, 2) + 3
            sleep_time = 2
            sleep(sleep_time)

        if lives == 0:
            # uid is '' some we return -1
            break

    return True, uuid


def submit_request(api_key: str, url: str):
    """
    Submit url to urlscan.
    """
    succ, uuid = post_to_url_scan(api_key, url)
    return succ, uuid

def read_request_from_db() -> tuple:
    succ, res = select_min_request(path)
    return succ, res


pid_manager = None
waiting_requests = []


def send_signal(pid: int):
    os.kill(pid, signal.SIGHUP)


def receive_signal(signum, stack):
    print('Preprocess: Received. ', signum)
    waiting_requests.append(signum)


def read_api_key() -> str:
    try:
        with open('api_key.txt') as f:
            api_key = f.readlines()
        f.close()
    except:
        print('Error: Can not read API KEY for url scan.')
        raise IOError
    return api_key[0]


def create_pid_file(pid: int):
    with open('pid.log', 'w') as f:
        f.write(str(pid))
    f.close()


def read_main_pid() -> int:
    """
    Read pid of main process.
    """
    with open(path + 'detection_systems/pid.log') as f:
        pid = f.readline()
    f.close()
    print('Reading pid of main process: {}'.format(pid))
    return int(pid)


def main():
    api_key = read_api_key()
    pid_manager = read_main_pid()
    my_pid = os.getpid()
    create_pid_file(my_pid)
    signal.signal(signal.SIGHUP, receive_signal)
    while True:
        if len(waiting_requests) == 0:
            print('Preprocess : No requests. PID is: {}. Number requests: {}'.format(my_pid, len(waiting_requests)))
            sleep(5)
        else:
            succ, res = read_request_from_db()
            (url, host_ip, minimal_id) = res
            succ, uid = submit_request(api_key, url)
            if succ:
                waiting_requests.pop()
                # delete_row(path, minimal_id)
                """
                Send signal to preprocess.
                """
                send_signal(pid_manager)
                print('Signal sent to manager.')
                update_submit(path, minimal_id)
                add_row(path, url, uid, host_ip)
            else:
                """
                URL is not valid..
                """
                print('This url {} is not valid. Saving to database.')
                db_manager.add_row(path, url, host_ip, 2)


if __name__ == '__main__':
    main()