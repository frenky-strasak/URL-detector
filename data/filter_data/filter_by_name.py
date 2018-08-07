""""
This script takes
"""

import sys


def read_alexa_top():
    alexa_dns_dict = {}
    with open('alexa_top_1000') as f:
        for line in f:
            dns_query = line.rstrip()
            alexa_dns_dict[dns_query] = 1
    f.close()
    return alexa_dns_dict


def save_new_dns_output(dns_list):
    with open('dns_file_output_filetr_1', 'w') as f:
        for dns in dns_list:
            f.write('{}\n'.format(dns))
    f.close()


def is_in_alexa_1000(dns, alexa_dns_dict):
    for alexa_dns in alexa_dns_dict.keys():
        if alexa_dns in dns:
            if alexa_dns == dns:
                return True
            if '.' + alexa_dns in dns:
                return True
            if alexa_dns + '.' in dns:
                return True
            if '.' + alexa_dns + '.' in dns:
                return True
    return False


def main(path_to_dns_file):

    alexa_dns_dict = read_alexa_top()

    dns_list = []
    index = 0
    i = 0

    with open(path_to_dns_file + 'dns_file_output') as f:
        for line in f:
            dns = line.rstrip()

            if is_in_alexa_1000(dns, alexa_dns_dict):
                # url is in alexa 1000
                index += 1
                print('{} {}'.format(index, dns))
            else:
                # url is not alexa top
                dns_list.append(dns)

            i += 1
    f.close()

    save_new_dns_output(dns_list)

    print('normal urls: {}'.format(index))
    print('all urls: {}'.format(i))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Error: No argument as path.')
