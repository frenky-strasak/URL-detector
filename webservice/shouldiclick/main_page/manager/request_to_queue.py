import os
import signal

from database.request_queue_db import add_row
from database.request_queue_db import select_request
from database.user_ip_db import delete_all_rows

path = '/'.join(os.getcwd().split('/')[:-2]) + '/'


def check_for_limit_user_ips(last_user_id: int):
    print('Deleting all user ips i checking db. ID of last user ip row is: {}:'.format(last_user_id))
    if last_user_id % 1000 == 999:
        delete_all_rows(path)


def write_request_to_databse(url: str, user_ip: str):
    succ = add_row(path, url, user_ip)
    return succ


def send_signal(pid: int):
    os.kill(pid, signal.SIGHUP)


def already_requested(url: str) -> bool:
    request_is_waiting, _ = select_request(path, url)
    if request_is_waiting:
        return True
    return False


def solve_request(pid: int, url: str, user_ip: str):
    if already_requested(url):
        print('Request is already in queue.')
        return 15
    succ = write_request_to_databse(url, user_ip)
    if succ:
        """
        Send signal to preprocess.
        """
        send_signal(pid)
        print('Signal sent to preprocess.')
    else:
        print('#######################')
        print('Error: request from user was not writen into database.')
        print('########################')

    return 45