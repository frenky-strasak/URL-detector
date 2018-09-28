"""
This script downloads json output from urlscan.io.
input: path to folder where alive and labeled url files are.
"""

import sys
import os
import requests
import urllib.request
from time import sleep
import json

sep = '\x09'


def read_data(path_to_url_file: str, url_list: list) -> None:
    with open(path_to_url_file) as f:
        for line in f:
            if line == '' or line[0] == '#':
                continue
            splited = line.rstrip().split(sep)
            url = splited[0].lower()
            # url = url.replace('www.', '')
            url_list.append(url)
    f.close()


def connect(headers: dict, data: str) -> tuple:
    try:
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=data)
        return True, response
    except:
        return False, ''

def ask_for_uuid(url: str, api_key: str) -> str:
    headers = {
        'Content-Type': 'application/json',
        'API-Key': api_key,
    }
    data = '{"url": "' + url + '", "public": "on"}'

    response = ''
    dead = 0
    is_connect = False
    while dead < 10:
        succ, response = connect(headers, data)
        if succ:
            is_connect = True
            break
        dead += 1
        sleep(5)
        print('         <<< Repeating connection...')

    if is_connect is False:
        print('Error: We have problems to connect to urlscan. Check your connection. Terminating.')
        sys.exit(1)

    # response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=data)
    print(response)
    try:
        res_dict = dict(response.json())
    except:
        uuid = None
        print(response.text)
        return uuid
    try:
        uuid = res_dict['uuid']
    except KeyError:
        uuid = None
        print(response.text)
    return uuid


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


def save_file(data: str, save_path: str):
    with open(save_path, 'w') as f:
        f.write(data)
    f.close()


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


def download_one_json(uuid: str, save_path: str,) -> bool:
    urlscan_request = 'https://urlscan.io/api/v1/result/' + uuid + '/'
    json_data = get_json_data(urlscan_request)
    if json_data == '':
        return False
    json_dict = json.loads(json_data)
    if data_ready(json_dict):
        save_file(json_data, save_path)
        return True
    else:
        return False


def download_stuff(uuid_dict: dict, error_url_dict: dict, error_url_get: dict, save_path: str, depth: int, file_index: int) -> None:
    """Download data from urlscan."""
    print(' << We are in depth {}'.format(depth))
    _threshold = 20
    if depth > _threshold:
        return
    not_succ = 0
    for url, uuid in uuid_dict.items():
        if uuid is None:
            if depth == _threshold:
                try:
                    error_url_dict[file_index].append((url, uuid))
                except:
                    error_url_dict[file_index] = []
                    error_url_dict[file_index].append((url, uuid))
            continue
        if uuid == -1:
            continue
        was_succ = download_one_json(uuid, save_path + '/' + url + '.json')
        if was_succ is False:
            if depth == _threshold:
                try:
                    error_url_get[file_index].append((url, uuid))
                except:
                    error_url_get[file_index] = []
                    error_url_get[file_index].append((url, uuid))
            not_succ += 1
        else:
            uuid_dict[url] = -1
    if not_succ != 0:
        sleep(20)
        download_stuff(uuid_dict, error_url_dict, error_url_get, save_path, depth + 1, file_index)


def print_error_urls(error_url_dict: dict) -> None:
    if len(error_url_dict.keys()) == 0:
        print('We have json files for every url. :]')
    else:
        print('##################')
        print('Problem urls:')
        all_problem_urls = 0
        for key, item in error_url_dict.items():
            print('{:04d}'.format(key))
            for url in item:
                print('  <<< {}'.format(url))
                all_problem_urls += 1
        print('################')
        print('In total we have error with {} urls.'.format(all_problem_urls))


def check_folders(save_path: str, file_index: int):
    """Create folder for json file."""
    folder_name = '{:04d}'.format(file_index)
    save_path = save_path + '/' + folder_name
    if os.path.exists(save_path):
        print('Error: This folder already exist {}. Terminating.'.format(folder_name))
        sys.exit(1)
    else:
        os.makedirs(save_path)
    return save_path


def post_urls(input_file_index, url_list: list, uuid_dict: dict, api_key: str) -> None:
    """Go though urls and make post request to urlscan."""
    url_list_len = len(url_list)
    for i, url in enumerate(url_list):
        print('{} - {}/{} We are posting: {} '.format(input_file_index, i, url_list_len, url), end='')
        uuid = ask_for_uuid(url, api_key)
        if uuid_dict.get(url, -1) == -1:
            uuid_dict[url] = uuid
        else:
            print('Error: Same urls. Clean your dataset and the do stuff. Exiting the script.')
            sys.exit(1)
        sleep(3)


def main(file_index: int, path_to_labeled_file: str, save_path: str, api_key: str, error_url_post: dict,
         error_url_get: dict) -> None:

    print('We are processing capture {}'.format(file_index))
    url_list = []
    uuid_dict = {}

    """Read data from url_file."""
    read_data(path_to_labeled_file, url_list)
    """Check if our folder already exists."""
    save_path = check_folders(save_path, file_index)
    """Post urls to urlscan."""
    post_urls(file_index, url_list, uuid_dict, api_key)
    """Wait some time for urlscan server."""
    sleep(10)
    """Download jsons, html from urlscan"""
    download_stuff(uuid_dict, error_url_post, error_url_get, save_path, 0, file_index)


def write_errors(error_url_post: dict, error_url_get: dict, file_name: str) -> None:
    print('#######################################################')
    if len(error_url_post.keys()) != 0:
        print('     << Error: Post requests are NOT ok. Look at the log files.')
        for key, item in error_url_post.items():
            with open('error_file_post_' + str(key) + '.txt', 'w') as f:
                f.write('# post errors\n')

                f.write('<<< file name: ' + str(key) + '\n')
                for url in item:
                    f.write(str(url[0]) + ' ' + str(url[1]) + '\n')
            f.close()
    else:
        print('     << Post requests are ok.')

    if len(error_url_get.keys()) != 0:
        print('     << Error: Get requests are NOT ok. Look at the log files.')
        for key, item in error_url_get.items():
            with open('error_file_get_' + str(key) + '.txt', 'w') as f:
                f.write('# get errors\n')
                f.write('<<< file name: ' + str(key) + '\n')
                for url in item:
                    f.write(str(url[0]) + ' ' + str(url[1]) + '\n')
            f.close()
    else:
        print('     << Get requests are ok.')


if __name__ == '__main__':
    print('Welcome in download manager for json by https://urlscan.io')
    print('First argument is API KEY.')
    print('Second argument is path to FILE where labeled urls are stored. If you want to process more files, put'
          'integer to loop in the code.')
    print('Third argument is path to FOLDER where json files should be saved.')
    print('#########################################\n')

    if len(sys.argv) == 4:
        api_key = sys.argv[1]
        path_to_url_file = sys.argv[2]
        save_path_to_folder = sys.argv[3]

        file_name = os.path.basename(path_to_url_file)
        file_index = int(file_name.replace('_html_labeled.txt', ''))

        path_to_input_folder = os.path.dirname(path_to_url_file)
        error_url_post = {}
        error_url_get = {}
        # (file_index+1) mean only 1 input file inside the loop.
        for i in range(file_index, file_index + 1):
            new_name = path_to_input_folder + '/' + '{:04d}'.format(i) + '_html_labeled.txt'
            main(i, new_name, save_path_to_folder, api_key, error_url_post, error_url_get)

        """Print non-successfully urls."""
        # print_error_urls(error_url_post)
        write_errors(error_url_post, error_url_get, file_name)
    else:
        print('Error: Amount of arguments is wrong.')

