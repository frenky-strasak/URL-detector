"""
This script takes list of url and try to find out if url is alive.
If url is alive so the html source of url is downloaded.
Argument: file with urls
"""

import urllib.request
import sys
from time import time
import os


def save_new_dns_output(dns_list: list, out_path_to_alive_url_dataset: str):
    with open(out_path_to_alive_url_dataset, 'w') as f:
        for dns in dns_list:
            f.write('{}\n'.format(dns))
    f.close()


def read_read_dns(path, dns_list):
    # Each line is one url.
    with open(path) as f:
        for line in f:
            dns = line.rstrip().lower()
            if dns == '':
                continue
            dns_list.append(dns)
    f.close()


def download_html(url, html_name, urlib_instant):
    # print('downloaded url: {}'.format(url))
    is_html_ok = True
    try:
        # html = urllib.request.urlopen('http://' + url).read().decode('utf-8')
        html = urlib_instant.read().decode('utf-8')
    except:
        try:
            # html = urllib.request.urlopen('http://' + url).read().decode("ISO-8859-1")
            html = urlib_instant.read().decode("ISO-8859-1")
        except:
            is_html_ok = False
            html = ''
            html_name += '_false'

    if is_html_ok:
        # if is_html_ok:
        with open(html_name + '.txt', 'w') as f:
            f.write(html)
        f.close()
        return 0
    else:
        with open(html_name + '.txt', 'w') as f:
            f.write('False\n' )
            f.write('http://' + url + 'does not work\n')
        f.close()
        return 1


def check_dns_alive(url):
    # print(urllib.request.urlopen("http://google.com").getcode())
    # if 'www.' not in url:
    #     url = 'www.' + url
    try:
        # returned_code = urllib.request.urlopen('http://' + 'www.google.com').getcode()
        # returned_code = urllib.request.urlopen('http://' + url, timeout=10).getcode()
        urlib_instant = urllib.request.urlopen('http://' + url, timeout=5)
        returned_code = urlib_instant.getcode()
    except:
        return False, url, None

    if returned_code == 200:
        return True, url, urlib_instant
    return False, url, None


def main(index, in_path_to_url, out_path_to_html_dataset, out_path_to_alive_url_dataset, file_name):

    # Create folder for html files.
    if os.path.exists(out_path_to_html_dataset + '/' + file_name):
        print('Error: Output folder for html files has already exist. Check your settings. Name url list is: {}'.format(file_name))
        return -1
    else:
        os.makedirs(out_path_to_html_dataset + '/' + file_name)

    dns_list = []
    read_read_dns(in_path_to_url, dns_list)
    new_dns_list = []

    t1 = time()
    no_html = 0
    live_dns = 0
    for i, dns in enumerate(dns_list):
        is_alive, url, urlib_instant = check_dns_alive(dns)
        if is_alive:
            live_dns += 1
            new_dns_list.append(url)
            file_html_name = '{:04d}'.format(live_dns) + '_' + url.replace('www.', '')
            spec_out_path_to_html_dataset = out_path_to_html_dataset + '/' + file_name + '/' + file_html_name
            no_html += download_html(url, spec_out_path_to_html_dataset, urlib_instant)
            print('<{}> {:<5} {:<40}    ==>     Connection was establihed. Live:{}  No html:{}'.format(index, i, url, live_dns, no_html))
        else:
            print('<{}> {:<5} {:<40}    ==>     Connection was NOT establihed. Live:{}  No html:{}'.format(index, i, url, live_dns, no_html))

    save_new_dns_output(new_dns_list, out_path_to_alive_url_dataset + '/' + file_name + '.txt')
    print('Finished in {} hours'.format((time() - t1) / (60*60)))
    return 0


if __name__ == '__main__':
    print('Welcome in checker dns.')
    print('First arg: First argument is path to FILE where urls are stored. If you want to process more files, put'
          'integer to loop in code.')
    print('Second arg: Second argument is path to FOLDER where html folders should be saved. Html folder will contain hmtl files.')
    print('Third arg: Third argument is path to FOLDER where alive url are saved.')
    if len(sys.argv) == 4:

        orig_file_name = os.path.basename(sys.argv[1])

        file_index = int(orig_file_name.split('_url')[0])
        file_name = str(orig_file_name.split('_url')[0]) + '_html'
        in_path_to_url = sys.argv[1]
        path_to_url_folder = os.path.dirname(in_path_to_url)
        out_path_to_html_dataset = sys.argv[2]
        out_path_to_alive_url_dataset = sys.argv[3]
        # main(in_path_to_url, out_path_to_html_dataset, out_path_to_alive_url_dataset, file_name)

        main_t = time()
        for i in range(file_index, file_index + 1):
            new_file_name = '{:04d}'.format(i) + '_html'
            path_to_url_name = path_to_url_folder + '/' + '{:04d}'.format(i) + '_url'
            err_stat = main(i, path_to_url_name, out_path_to_html_dataset, out_path_to_alive_url_dataset, new_file_name)
            if err_stat == -1:
                break
        print('All process takes {} hours'.format((time() - main_t) / (60*60) ))
    else:
        print('Error: No arguments as paths. First argument is path to file where all url are stored. '
              'Second argument is path to folder where html folder should be saved. Html folder contains html files.'
              '. Third argument is path to folder where alive url are saved.')
