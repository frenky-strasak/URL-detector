import urllib.request
import sys


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
    print(url)
    try:
        # returned_code = urllib.request.urlopen('http://' + 'www.google.com').getcode()
        returned_code = urllib.request.urlopen('http://' + url).getcode()
    except:
        return False
    if returned_code == 200:
        return True
    return False


def main(path):
    dns_list = []
    read_read_dns(path, dns_list)

    new_dns_list = []
    for dns in dns_list:
        if check_dns_alive(dns):
            new_dns_list.append(dns)
            print(dns)

    save_new_dns_output(new_dns_list)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Error: No argument as path.')