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


def save_new_dns_output(dns_dict):
    with open('dns_file_output_filter_3', 'w') as f:
        for dns in dns_dict.keys():
            f.write('{}\n'.format(dns))
    f.close()


def is_in_alexa_1000(dns, alexa_dns_dict):
    if '.' not in dns:
        return True
    if '.arpa' in dns:
        return True
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

    dns_dict = {}
    index = 0
    i = 0

    with open(path_to_dns_file) as f:
        for line in f:
            dns = line.rstrip().lower()

            if is_in_alexa_1000(dns, alexa_dns_dict):
                # url is in alexa 1000
                index += 1
                print('{} {}'.format(index, dns))
            else:
                # url is not alexa top
                try:
                    dns_dict[dns] += 1
                    print('karlos chodi po schodech.............')
                except:
                    dns_dict[dns] = 1
            i += 1
    f.close()

    save_new_dns_output(dns_dict)

    print('normal urls: {}'.format(index))
    print('all urls: {}'.format(i))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Error: No argument as path.')
