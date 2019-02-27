import sys
import os
from time import time
# sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')

# sys.path.insert(0, '.')

from database.database_manager import update_feedback_row
from database.database_manager import delete_row
from database.database_manager import domain_has_label
from database.user_ip_db import select_request
from database.user_ip_db import add_row
from .request_to_queue import solve_request
from .request_to_queue import check_for_limit_user_ips

"""
Set PID of main process.
"""

path = '/'.join(os.getcwd().split('/')[:-2]) + '/'


def read_main_pid() -> int:
    """
    Read pid of main process.
    """
    with open(path + 'preprocess/pid.log') as f:
        pid = f.readline()
    f.close()
    print('Reading pid of preprocess: {}'.format(pid))
    return int(pid)

pid_preprocess = read_main_pid()


def attacked(user_ip: str):
    """
    Check the last request from this IP because of an attack.
    """
    t = time()
    succ, row = select_request(path, user_ip)
    print(succ, row)
    if succ is False:
        add_row(path, user_ip, t)
    else:
        check_for_limit_user_ips(row[0])
        last_request_from_user = float(row[1])
        if (t - last_request_from_user) < 1:
            """
            Attack is here.
            """
            return True
    return False


def get_decision(url: str, user_ip: str) -> tuple:
    """
    0 - url is normal,
    1 - url is malicious
    2 - url is not valid
    -10 - waiting for result
    -11 - attack is here
    :param url:
    :return:
    """

    if attacked(user_ip):
        return -11, None

    print('domain {}'.format(url))
    """
    Check if we have the domain in database.
    """
    has_label, label, ID = domain_has_label(path, url)
    if has_label:
        print('URL is already in database.')
        if label != 0 and label != 1 and label != 2:
            delete_row(path, ID)
        return int(label), None

    else:
        """
        If the requested domain is not in the database, create new threat to analyse it.
        Also send the waiting response to the client.
        """
        remaining_time = solve_request(pid_preprocess, url, user_ip)
        return -10, remaining_time


def save_feedback(url: str, user_ip: str, detection_result: int, feedback: int) -> int:
    print('Feedback function.......')
    if attacked(user_ip):
        return -11
    """
    Save feedback from user to feedback database.
    """
    update_feedback_row(path, url, user_ip, detection_result, feedback)
    return 0


if __name__ == '__main__':
    # url = 'www.seznam.cz'
    url = 'saloon26.ru'
    # url = 'ulice.nova.cy'
    # url = 'oaskdasda54asd.cz'
    res = get_decision(url, 'my_test_ip')
    print(res)