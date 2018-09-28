import random

import sys
sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
from manager.json_decision import get_decision_from_json


def get_decision(url: str):
    """
    0 - url is normal
    1 - url is malicious
    2 - url is not url
    :param url:
    :return:
    """
    result = get_decision_from_json(url)
    return result



if __name__ == '__main__':
    # url = 'www.seznam.cz'
    url = 'saloon26.ru'
    res = get_decision(url)
    print(res)