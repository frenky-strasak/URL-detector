"""
This script computes features for each sample
"""


import os
import sys
# sys.path.insert(0, '/home/frenky/PycharmProjects/url_detector/URL-detector/')
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-2]) + '/')
from detection_systems.url_json_analyzer import feature_vector
import numpy as np


def get_data(path_to_malware: str, path_to_normal: str):

    """
    Malware computing of features
        Empty jsons in malware: 140
        All malware jsons: 10258
    """
    empty_json_malware = 0
    all_malware = 0
    malware_list = []
    for folder_i, folder in enumerate(sorted(os.listdir(path_to_malware))):
        print(' << {}'.format(folder))
        for i, json in enumerate(sorted(os.listdir(path_to_malware + '/' + folder))):
            path_to_json = path_to_malware + '/' + folder + '/' + json
            print('malware {}:    <<< {} {}'.format(folder_i, i, path_to_json))
            succ, np_arr = feature_vector.get_feature_vector(path_to_json)
            if succ:
                all_malware += 1
                malware_list.append(np_arr)
            else:
                empty_json_malware += 1



    """
    Normal computing of features
        Empty jsons in normal: 330
        All normal jsons: 15830
    """
    empty_json_normal = 0
    all_normal = 0
    normal_list = []
    for folder_i, folder in enumerate(sorted(os.listdir(path_to_normal))):
        print(' << {}'.format(folder))
        for i, json in enumerate(sorted(os.listdir(path_to_normal + '/' + folder))):
            path_to_json = path_to_normal + '/' + folder + '/' + json
            print('normal {}:    <<< {} {}'.format(folder_i, i, path_to_json))
            succ, np_arr = feature_vector.get_feature_vector(path_to_json)
            if succ:
                all_normal += 1
                normal_list.append(np_arr)
            else:
                empty_json_normal += 1



    print('Empty jsons in malware: {}'.format(empty_json_malware))
    print('All malware jsons: {}'.format(all_malware))
    np.save('malware_json_features.npy', np.array(malware_list))

    print('Empty jsons in normal: {}'.format(empty_json_normal))
    print('All normal jsons: {}'.format(all_normal))
    np.save('normal_json_features.npy', np.array(normal_list))



if __name__ == '__main__':
    mal = '/home/frenky/Documents/Skola/Stratosphere_url_detector/final_data/data/output_data/malware/urlscan_json'
    norm = '/home/frenky/Documents/Skola/Stratosphere_url_detector/final_data/data/output_data/normal/urlscan_json'
    get_data(mal, norm)
