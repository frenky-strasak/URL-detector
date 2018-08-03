"""
Download single file.
USAGE: python download_single_file.py url_to_file path_to_save_file
"""


import wget
import ssl
import sys


def download_file(url: str, save_path: str):
    """
    :param url: str
    :param save_path: str
    :return: none
    """
    # make ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(url, save_path)
    print('')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        download_file(sys.argv[1], sys.argv[2])
    else:
        # raise Exception('No arguments')
        print('Please put arguments: first one is url, second one is path where file should be save.')