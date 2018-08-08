"""
This script takes list of url and try to find out if url is alive.
If url is alive so the html source of url is downloaded.
Argument: file with urls
"""

import urllib.request
from urllib.request import urlopen
import sys
from time import time


def save_new_dns_output(dns_list):
    with open('new_dns_file_output_filter', 'w') as f:
        for dns in dns_list:
            f.write('{}\n'.format(dns))
    f.close()


def read_read_dns(path, dns_list):
    # Each line is one url.
    with open(path) as f:
        for line in f:
            dns = line.rstrip()
            dns_list.append(dns)
    f.close()


def download_html(url, html_name):
    # print('downloaded url: {}'.format(url))
    try:
        html = urlopen('http://' + url).read().decode('utf-8')
    except:
        try:
            html = urlopen('http://' + url).read().decode("ISO-8859-1")
        except:
            html = urlopen('http://' + url).read()
            html_name += '_encoded'

    # print(html)
    with open(html_name, 'w') as f:
        f.write(html)
    f.close()


def check_dns_alive(url):
    # print(urllib.request.urlopen("http://google.com").getcode())
    if 'www.' not in url:
        url = 'www.' + url

    try:
        # returned_code = urllib.request.urlopen('http://' + 'www.google.com').getcode()
        returned_code = urllib.request.urlopen('http://' + url).getcode()
    # except urllib.request.HTTPError:
    except:
        return False, url

    if returned_code == 200:
        return True, url
    return False, url


def main(path, path_to_dataset):

    dns_list = []
    read_read_dns(path, dns_list)
    new_dns_list = []

    t1 = time()

    live_dns = 0
    for i, dns in enumerate(dns_list):
        is_alive, url = check_dns_alive(dns)
        if is_alive:
            live_dns += 1
            new_dns_list.append(url)
            download_html(url, path_to_dataset + '/' + str(live_dns) + '_' + url.replace('www.', ''))
            print('{} {}    ==>     Connection was establihed. {}'.format(i, url, live_dns))
        else:
            print('{} {}    ==>     Connection was NOT establihed. {}'.format(i, url, live_dns))
        if live_dns > 5:
            break
    save_new_dns_output(new_dns_list)
    print('Finished in {} hours'.format((time() - t1) / (60*60)))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Error: No arguments as paths. First argument is path to file where all url are stored. Secon argument is'
              'path to folder, where html should be saved. List of live url is saved to same place like this script.')
