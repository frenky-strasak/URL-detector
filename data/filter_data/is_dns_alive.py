import urllib.request
import sys
from time import time


def save_new_dns_output(dns_list):
    with open('dns_file_output_filetr_2', 'w') as f:
        for dns in dns_list:
            f.write('{}\n'.format(dns))
    f.close()


def read_read_dns(path, dns_list):
    with open(path) as f:
        for line in f:
            dns = line.rstrip()
            dns_list.append(dns)
    f.close()


def check_dns_alive(url):
    # print(urllib.request.urlopen("http://google.com").getcode())
    if 'www.' not in url:
        url = 'www.' + url

    try:
        # returned_code = urllib.request.urlopen('http://' + 'www.google.com').getcode()
        returned_code = urllib.request.urlopen('http://' + url).getcode()
    except:
        return False, url

    if returned_code == 200:
        return True, url
    return False, url


def main(path):
    dns_list = []
    read_read_dns(path, dns_list)
    new_dns_list = []

    t1 = time()

    live_dns = 0
    for i, dns in enumerate(dns_list):
        is_alive, url = check_dns_alive(dns)
        if is_alive:
            new_dns_list.append(url)
            print('{} {}    ==>     Connection was establihed. {}'.format(i, url, live_dns))
            live_dns += 1
        else:
            print('{} {}    ==>     Connection was NOT establihed. {}'.format(i, url, live_dns))

    save_new_dns_output(new_dns_list)
    print('Finished in {} hours'.format((time() - t1) / (60*60)))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Error: No argument as path.')