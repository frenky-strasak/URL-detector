
import sys
sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
import random
import requests
import urllib.request
import json
from time import sleep
from detection_systems.url_json_analyzer.feature_vector import get_feature_vector
import xgboost as xgb
import pickle
from xgboost import XGBClassifier
from xgboost import Booster
import numpy as np

"""
Load xgboost model.
"""

# _xgboost_module = pickle.load(open("/home/frenky/PycharmProjects/url_detector/URL-detector/manager/xgboost_2018_09_27_21_56.sav", "rb"))


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
                sleep_time = random.uniform(0, 2) + 3
                sleep(sleep_time)
        else:
            print('sleeing in post 2')
            lives += -1
            sleep_time = random.uniform(0, 2) + 3
            sleep(sleep_time)

        if lives == 0:
            break

    return True, uuid


def get_json_data(urlscan_request: str):
    json = ''
    try:
        urlib_instant = urllib.request.urlopen(urlscan_request)
        try:
            json = urlib_instant.read().decode('utf-8')
        except:
            try:
                json = urlib_instant.read().decode("ISO-8859-1")
            except:
                pass
    except:
        pass
    return json


def data_ready(json: dict) -> bool:
    """
    If it is not ready: "status": 404
    If it is ready: (not key "status")
    """
    try:
        #
        status = json['status']
        status_int = status
        if status_int == 404:
            return False
        else:
            return False
    except:
        """
        There is no key "status", so it is ok.
        """
        return True


def download_one_json(uuid: str) -> tuple:
    urlscan_request = 'https://urlscan.io/api/v1/result/' + uuid + '/'

    json_data = get_json_data(urlscan_request)
    if json_data == '':
        return None, False
    json_dict = json.loads(json_data)
    if data_ready(json_dict):
        return json_dict, True
    else:
        return None, False


def download_json(uuid: str) -> tuple:
    lives = 5
    while True:
        json_dict, succ_down = download_one_json(uuid)
        if succ_down:
            return True, json_dict
        else:
            print('sleeping in downloading')
            sleep(3)
            lives += -1

        if lives == 0:
            return False, None


def get_input_json(api_key: str, url: str):
    valid_url, uuid = post_to_url_scan(api_key, url)
    if valid_url is False:
        return 2, None

    if uuid == '':
        return -1, None

    sleep(2)

    succ, json_dict = download_json(uuid)

    if succ is False:
        return -1, None

    return 0, json_dict


def get_decision_from_json(url: str) -> int:
    api_key = ''
    succ, json_dict = get_input_json(api_key, url)
    if succ == 2 or succ == -1:
        return succ

    print('computing features')
    # print(json_dict)
    succ, sample_1 = get_feature_vector(json_data=json_dict)
    if succ is False:
        return 3

    path_to_model = '/home/frenky/PycharmProjects/url_detector/URL-detector/manager/xgboost_2018_09_28_11_18.sav'
    # path_to_model = '/home/frenky/PycharmProjects/url_detector/URL-detector/manager/random_forest_2018_09_28_11_40.sav'
    _xgboost_module = pickle.load(open(path_to_model, "rb"))
    result_1 = _xgboost_module.predict(np.array([sample_1]))
    print('resutlt for {} is : {}'.format(url, result_1[0]))
    # print(sample)
    return int(result_1[0])