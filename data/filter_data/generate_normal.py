
import sys
import pandas as pd
import csv
from tld import get_tld


"""
1082669 - 1082613
"""

def write(url_list: list) -> None:
    save_path = '/home/frenky/Documents/Skola/Stratosphere_url_detector/data/normal/filtered_and_splited/'
    with open(save_path + '/normal_dns_filtered_2.txt', 'w') as f:
        for dns in url_list:
            f.write('{}\n'.format(dns))
    f.close()


def filter(url: str) -> bool:
    # if 'google.com.' in url:
    #     # print(url)
    #     return False
    if 'porn' in url:
        # print(url)
        return False
    if 'sex' in url:
        # print(url)
        return False
    if 'xx' in url:
        # print(url)
        return False
    return True


def get_key_url(url: str) -> tuple:
    right_url = 'http://www.' + url
    try:
        top_level_domain = get_tld(right_url)
        url = url.replace(top_level_domain, '')
        return True, url
    except:
        print('This url does not have {}'.format(url))
        return False, url


def read_cvs_and_csv(path_1_csv: str, path_2_csv: str):
    threshold = 500000
    index = 0
    last_index_1 = 0
    last_index_2 = 0
    normal_url_dict = {}
    url_list = []
    with open(path_1_csv) as csv_reader:
        spamreader = csv.reader(csv_reader, delimiter=',', quotechar='|')
        for line in spamreader:
            last_index_1 += 1
            url = line[1].rstrip().lower().replace('www.', '')
            right_url, url_key = get_key_url(url)
            if right_url is False:
                continue
            if filter(url_key) is False:
                continue
            try:
                normal_url_dict[url_key] += 1
                continue
            except:
                normal_url_dict[url_key] = 1
                url_list.append(url)

            index += 1
            if index > threshold:
                break

    csv_reader.close()

    print('---------------')
    index = 0
    with open(path_2_csv) as csv_reader:
        spamreader = csv.reader(csv_reader, delimiter=',', quotechar='|')
        for line in spamreader:
            last_index_2 += 1
            url = line[1].rstrip().lower().replace('www.', '')
            right_url, url_key = get_key_url(url)
            if right_url is False:
                continue
            if filter(url_key) is False:
                continue
            try:
                normal_url_dict[url_key] += 1
                continue
            except:
                normal_url_dict[url_key] = 1
                url_list.append(url)

            index += 1
            if index > threshold:
                break

    csv_reader.close()

    print('We have {} urls.'.format(len(normal_url_dict.keys())))
    print('we red {} and {} urls'.format(last_index_1, last_index_2))
    write(url_list)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        path_1 = sys.argv[1]
        path_2 = sys.argv[2]
        # read_cvs_and_txt(path_1, path_2)
        read_cvs_and_csv (path_1, path_2)
    else:
        print('Wrong arguments.')
