"""
This script is for labeling url by virus total. You need virus total API KEY and list urls to label.
You can choose if you wan to label normal url or malware url. The different is that for normal labeling it creates
file_labeled with only normal url. Same way for malware labeling.
"""

import requests
import sys
import os
from time import time
from time import sleep


verbose_msg_post = 'Scan request successfully queued, come back later for the report'
verbose_msg_success = 'Scan finished, scan information embedded in this object'

vir_total_url = 'https://www.virustotal.com/vtapi/v2/url/report'
sep = '\x09'


def write_output(path: str, data_dict: dict, still_waiting_response: int) -> None:
    for html_file, d in data_dict.items():
        new_name = html_file.replace('.txt', '')
        with open(path + '/' + new_name + '_labeled.txt', 'w') as f:
            f.write('# Dataset of url. Part of URL-Detector project. '
                    'In case of next information contact: strasfra_fel.cvut.cz\n')
            f.write('# separator: <backslash>x09\n')
            f.write('# number of waiting urls for virus total: {}\n'.format(still_waiting_response))
            f.write('# Fields: url, positives, antivirus_number, label, antivirus_names\n')

            # Labeling malware.
            for key, tuple in d.items():
                if tuple == '':
                    # normal url.
                    continue
                elif tuple is not False:
                    # url is malware.
                    text = ''
                    text += tuple[0] + sep + tuple[1] + sep + tuple[2] + sep + tuple[3] + sep
                    text += '[' + ','.join(tuple[4]) + ']'
                    f.write(text + '\n')
                elif tuple is False:
                    # We are waiting for but we can not more.
                    f.write(key + ',waiting_for_post')
        f.close()


def check_existing_labeled(out_path: str, start_file: str, end_file: str) -> bool:
    """
    Check if files for labeling are not already labeled.
    """
    start_index = int(start_file.replace('_html.txt', ''))
    end_index = int(end_file.replace('_html.txt', ''))
    for file in os.listdir(out_path):
        file_index = int(file.replace('_html_labeled.txt', ''))
        if start_index <= file_index <= end_index:
            print('Error: This file {} is already labeled. Check your range of number of files.'.format(file))
            return False
    return True


def read_files(path: str, data_dict: dict, start_file: str, end_file: str) -> int:
    """
    Read all files in folder.
    """
    start_index = int(start_file.replace('_html.txt', ''))
    end_index = int(end_file.replace('_html.txt', ''))
    total_urls = 0
    for file in os.listdir(path):
        file_index = int(file.replace('_html.txt', ''))
        if start_index <= file_index <= end_index:
            data_dict[file] = {}
            d = {}
            with open(path + '/' + file) as f:
                for line in f:
                    if line == '' or line[0] == '#':
                        continue
                    data_dict[file][line.rstrip().lower()] = ''
                    try:
                        d[line.rstrip().lower()] += 1
                    except:
                        d[line.rstrip().lower()] = 1
            f.close()
            print(' <<<< {} Info: We have {} urls.'.format(file, len(d.keys())))
            total_urls += len(d.keys())
    return total_urls


def request_to_virus_total(url_to_scan: str, api_key: str) -> dict:
    params = {'apikey': api_key, 'resource': url_to_scan,
              'scan': 1}
    response = requests.get(vir_total_url, params=params)
    return dict(response.json())


def get_list_positive_antiviruses(dict_response: dict, positives_total: int) -> list:
    antivirus_name_list = []
    positie = 0
    scans_dict = dict_response['scans']
    for key, item in scans_dict.items():
        detected = item['detected']
        if detected is True:
            antivirus_name_list.append(key)
            positie += 1
        if positie == positives_total:
            break
    return antivirus_name_list


def get_virus_total_status(url_to_scan: str, api_key: str) -> tuple:
    dict_response = request_to_virus_total(url_to_scan, api_key)
    response_code = int(dict_response['response_code'])

    if response_code == 1:
        """
        As we tried there are 2 options with reponse code == 1:
        1. We get data
        2. We have to ask again (wait few seconds (it works after ~2 seconds)). It seems to similar to response code 0.
        """
        try:
            verbose_msg = dict_response['verbose_msg']
            if verbose_msg == verbose_msg_success:
                positives = int(dict_response['positives'])
                total_anti = int(dict_response['total'])
                anti_list = get_list_positive_antiviruses(dict_response, positives)
                return response_code, 0, positives, total_anti, '', anti_list
            elif verbose_msg == verbose_msg_post:
                url_to_return = dict_response['permalink']
                return response_code, 1, 0, 0, url_to_return, []
            else:
                return response_code, 2, 0, 0, '', []
        except KeyError as e:
            print('Error: We got response_code 1 however there is no key: {}'.format(e))
            # sys.exit(1)

    elif response_code == 0:
        """
        According virus total documentation (https://www.virustotal.com/en-gb/documentation/public-api/#getting-url-scans)
        it means that url is not present in VirusTotal's dataset. 
        """
        try:
            url_to_return = dict_response['permalink']
        except KeyError as e:
            print('Error: We got response_code 0 however there is no key: {}'.format(e))
            # sys.exit(1)
        return response_code, 1, 0, 0, url_to_return, []
    elif response_code == -2:
        """
        We are still waiting for analysis. Wait!
        """
        try:
            url_to_return = dict_response['permalink']
        except KeyError as e:
            print('Error: We got response_code -2 however there is no key: {}'.format(e))
            # sys.exit(1)
        return response_code, 1, 0, 0, url_to_return, []
    else:
        print('Error: we do not know this response_code: {}'.format(response_code))
        # sys.exit(1)
        return response_code, 2, 0, 0, None, []


def main(api_key: str, path_to_folder: str, save_path: str) -> None:
    # Keep names of files and their captures.
    data_dict = {}
    # Url for later processing.
    post_url = []
    unknown_reponse = 0
    still_waiting_response = 0

    ##########################################
    """
    Say which files you want to process.
    """
    first_file = '0013_html.txt'
    last_file = '0013_html.txt'
    ###########################################

    if check_existing_labeled(save_path, first_file, last_file) is False:
        return
    total_urls = read_files(path_to_folder, data_dict, first_file, last_file)
    print('We are going to process these files: from {} to {}'.format(first_file, last_file))
    print('Total amount of url for requesting virus total is: {}'.format(total_urls))
    input("Press Enter to continue... ")
    index = 0
    positive_index = 0
    start_t = time()
    for html_file, d in data_dict.items():
        print('<< {}'.format(html_file))
        for url in d.keys():
            index += 1
            # print(url)
            response_code, error_code, positives, total_anti, post_url_to_connect, anti_list = get_virus_total_status(url, api_key)
            if error_code == 0:
                if positives > 0:
                    data_dict[html_file][url] = (url, str(positives), str(total_anti), '1', anti_list)
                    positive_index += 1
            elif error_code == 1:
                post_url.append((html_file, url, post_url_to_connect))
            else:
                unknown_reponse += 1
            print('     <<< {}/{:<15}       {:<40}   response: {:<25}   error_code: {}'.format(index, total_urls, url, response_code, error_code))
            # sleep(0.05)

    posted_url = len(post_url)
    print(' * We are starting to process url that was posted: {}'.format(posted_url))
    sleep(10)
    # Process urls that we had to wait until virus total process them.
    for item in post_url:
        html_file, url, post_url_to_connect = item
        response_code, error_code, positives, total_anti, post_url_to_connect, anti_list = get_virus_total_status(url, api_key)
        if error_code == 0:
            if positives > 0:
                data_dict[html_file][url] = (url, str(positives), str(total_anti), '1', anti_list)
                positive_index += 1
        else:
            data_dict[html_file][url] = False
            still_waiting_response += 1

    write_output(save_path, data_dict, still_waiting_response)

    print('\n##############################################')
    print('Number of unknown_reponse: {}'.format(unknown_reponse))
    print('Urls to posted: {}'.format(posted_url))
    print('Number of still waiting response (not finished yet): {}'.format(still_waiting_response))
    print('All requested url: {} / {}'.format(index, positive_index))
    print('Total time: {} hours'.format((time() - start_t) / 3600.0))

if __name__ == '__main__':
    """
    Arguments:
    1. api key to virus total.
    2. path to folder where url files are.
    3. path to folder where labeled url files should be saved.
    4. Choose if you want to label normal or malware. It creates labeled file, where normal/malware will be. The 
       argument is bool (False, True).  True -> normal labeling, False - malware labeling.
    """
    print('Welcome in virus total script. This script is for requesting url. The first argument is virus total API key.'
          'Second argument is path to FOLDER where input files with url are. Third argument is path to FOLDER where '
          'to store labeled urls in files. Also you have to specify which files you have to label in the source code.')
    print('#################################\n\n')
    if len(sys.argv) == 4:
        api_key = sys.argv[1]
        path_to_folder = sys.argv[2]
        output_path = sys.argv[3]
        main(api_key, path_to_folder, output_path)
    else:
        print('Error: We need more or less arguments.')
