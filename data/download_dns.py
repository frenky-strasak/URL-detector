"""
Connect to https://mcfp.felk.cvut.cz/publicDatasets/ and take dns names from bro dns.logs from each capture.
USAGE: python -W ignore download_dns.py
"""

from bs4 import BeautifulSoup
import requests
import urllib.request
import ssl
import urllib
from time import time


def save_dns_to_file(dns_dict: dict):
    with open('dns_file_output', 'w') as f:
        for key in dns_dict.keys():
            f.write('{}\n'.format(key))
    f.close()


def get_dns_from_file(url: str, dns_dict: dict):
    """
    In dataset there are 2 versions of bro. First version of bro does have feature 'rtt' and second version has it.
    So we have to find out which version of bro is here because of index of dns 'dns_index'.
    More information: https://www.bro.org/sphinx/scripts/base/protocols/dns/main.bro.html#type-DNS::Info
    :param dns_dict:
    :param url: str
    :return: none
    """
    dns_index_founded = False
    dns_index = 0

    content = urllib.request.urlopen(url)
    for line in content:
        # Decode line ( \t -> '    ').
        decoded_line = line.rstrip().decode()
        if dns_index_founded is False:
            if 'field' in decoded_line:
                if 'rtt' in decoded_line:
                    dns_index = 9
                else:
                    dns_index = 8
                dns_index_founded = True
        else:
            # We have already know 'dns_index' and we read data.
            if decoded_line[0] == '#':
                continue

            dns = decoded_line.split('	')[dns_index]
            dns_dict[dns] = 1


def find_files(url: str):
    soup = BeautifulSoup(requests.get(url, verify=False).text, "lxml")
    hrefs = []
    for a in soup.find_all('a'):
        try:
            hrefs.append(a['href'])
        except:
            print('Error: no href. Look at function: find_files.')
    return hrefs


def gel_all_dns(url: str):
    capture_names = find_files(url)

    # Make ssl for connecting https.
    ssl._create_default_https_context = ssl._create_unverified_context

    # Dictionary with all dns.
    dns_dict = {}

    main_t = time()
    not_dns_log_list = []
    x = 0
    # Go through all captures in dataset.
    for i in range(len(capture_names)):
        if 'CTU-Malware-Capture-Botnet-' in capture_names[i]:
            print('----------------------')
            print('{}'.format(capture_names[i]))
            print('----------------------')
            time_cap = time()
            # Get content of the main page of dataset.
            content = find_files(url + capture_names[i])
            # Look into open folder to files there. There are binetflow, bro, ...
            # And find the bro folder in this list.
            try:
                get_dns_from_file(url + capture_names[i] + '/bro/' + 'dns.log', dns_dict)
            except urllib.request.HTTPError:
                print('Error: there is no dns.log probably.')
                not_dns_log_list.append(capture_names[i])

            # for j in range(len(content)):
            #     if 'bro' in content[j]:
            #         # We found bro folder.
            #         try:
            #             get_dns_from_file(url + capture_names[i] + content[j] + 'dns.log', dns_dict)
            #         except ConnectionError:
            #             print('Error: there is no dns.log probably.')
            #             not_dns_log += 1
            #         break
            print('     << dataset finished in {} seconds or {} minutes'.format((time() - time_cap), (time() - time_cap) / 60.0))
            # x += 1
            # if x > 6:
            #     break
    # Print all gathered dns.
    save_dns_to_file(dns_dict)
    print('number of all domains: {}'.format(len(dns_dict.keys())))
    print('All process takes {} hours.'.format((time() - main_t) / (60 * 60)))
    print('Problem captures are:')
    print(not_dns_log_list)


def main():
    dataset_url = "https://mcfp.felk.cvut.cz/publicDatasets/"
    gel_all_dns(dataset_url)

if __name__ == '__main__':
    main()
