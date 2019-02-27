import signal
import os
import time
import sys

# sys.path.insert(0, '..')
path = '/'.join(os.getcwd().split('/')[:-1]) + '/'
sys.path.insert(0, path)
# sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/' + 'database/')


from database.request_submited_queue_db import select_min_request
from database.request_submited_queue_db import delete_row
import database.request_queue_db as base_db
from database.database_manager import add_row

from detection_systems.json_decision import get_decision_from_json


waiting_requests = []


def call_detectors(url: str, uuid: str):
    """
    1. Call detector based on json from urlscan.
    """
    result = get_decision_from_json(url, uuid)

    return result


def read_request_from_db() -> tuple:
    succ, res = select_min_request(path)
    return succ, res


def receive_signal(signum, stack):
    print('Received:', signum)
    waiting_requests.append(signum)


def create_pid_file(pid: int):
    with open('pid.log', 'w') as f:
        f.write(str(pid))
    f.close()


def main():
    signal.signal(signal.SIGHUP, receive_signal)
    my_pid = os.getpid()
    create_pid_file(my_pid)
    print('Manager PID is: {}'.format(my_pid))
    while True:

        if len(waiting_requests) == 0:
            print('No requests. PID is: {}. Number requests: {}'.format(my_pid, len(waiting_requests)))
            time.sleep(5)
        else:
            print('######## New request #######')
            print('my pid: {}'.format(my_pid))
            print('Number requests: {}'.format(len(waiting_requests)))
            t1 = time.time()

            succ, res = read_request_from_db()
            (url, uuid, host_ip, minimal_id) = res

            print('url: {}'.format(url))
            print('user ip: {}'.format(host_ip))

            result = call_detectors(url, uuid)
            add_row(path, url, host_ip, result)
            delete_row(path, minimal_id)
            base_db.delete_row_by_url(path, url)
            waiting_requests.pop()
            print('Total time for this request is {}'.format(time.time() - t1))


if __name__ == '__main__':
    main()
    # print(sys.path)
    # print('/'.join(os.getcwd().split('/')[:-1]) + '/')
    # domain_has_label(path, 'pornhub.com')
