"""
This script downloads json output about website from urlscan.io.

argument: 'url'
"""

import sys


def main(url):
    print(url)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('No url as argument.')

