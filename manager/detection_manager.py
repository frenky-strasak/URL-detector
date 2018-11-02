import random

import sys
sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
from manager.json_decision import get_decision_from_json
from manager.database.database_manager import add_row
from manager.database.database_manager import domain_has_label
from manager.database.database_manager import update_feedback_row


def get_decision(url: str, user_ip: str) -> int:
    """
    0 - url is normal,
    1 - url is malicious
    2 - url is not valid
    :param url:
    :return:
    """
    # Check if have the domain in database.
    has_label, label = domain_has_label(url)
    if has_label:
        return int(label)
    # get detection result
    result = get_decision_from_json(url)
    # save into database
    add_row(url, user_ip, result)
    return result


def save_feedback(url: str, user_ip: str, detection_result: int, feedback: int) -> None:
    # print(url, user_ip, detection_result, feedback)
    update_feedback_row(url, user_ip, detection_result, feedback)


if __name__ == '__main__':
    # url = 'www.seznam.cz'
    url = 'saloon26.ru'
    # url = 'ulice.nova.cy'
    # url = 'oaskdasda54asd.cz'
    res = get_decision(url, 'my_test_ip')
    print(res)