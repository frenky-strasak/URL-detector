"""
Temporal file.
"""


import sys
import os

path_to_url_folder = sys.argv[1]


dict_files = {}
list_files = []

all_dict = {}
big_hit = 0
big_index = 0


for file in os.listdir(path_to_url_folder):
    dict_files[file] = {}
    hit = 0
    index = 0

    with open(path_to_url_folder + '/' + file) as f:
        for line in f:
            url = line.strip().lower()
            try:
                dict_files[file][url] += 1
                hit += 1
            except:
                dict_files[file][url] = 1
            index += 1

            try:
                all_dict[url] += 1
                big_hit += 1
            except:
                all_dict[url] = 1
            big_index += 1

    list_files.append((file, hit, index))


print('conclusion:')
for tuple in list_files:
    print('{}   {}/{}'.format(tuple[0], tuple[1], tuple[2]))

print('All {}/{}'.format(big_hit, big_index))