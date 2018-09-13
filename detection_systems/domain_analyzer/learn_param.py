"""
Script for detecting generated url. (read data, feature selection, machine learning)
Input: list of words
Output: Learned model

Features: probabilistic model of normal english words, occurrences of diphthongs, etc.
"""


import numpy as np
import matplotlib.pyplot as plt
from tld import get_tld
import random


from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_gaussian_quantiles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


wovel_list = ['A', 'E', 'I', 'O', 'U', 'Y']
wovel_list_lower = ['a', 'e', 'i', 'o', 'u', 'y']
consonant_list = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z']
consonant_list_lower = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']


def remove_top_level_domain(host_name: str):
    """
    Remove top level domain from url.
    Example: input: 'facebook.com' -> return: 'facebook'
    :param host_name:
    :return:
    """
    top_domain = get_tld(host_name, fix_protocol=True)
    host_name = host_name.replace(top_domain, '')
    return host_name


def create_diphthongs(diphthong_dict: dict):
    """
    Create diphthongs from list of consonant and from list of wovel.
    Example: 'b' + 'a' -> 'ba', 'b' + 'e' -> 'be', etc.
    :param diphthong_dict:
    :return:
    """
    for c in consonant_list:
        for w in wovel_list:
            diphthong_dict[c.lower() + w.lower()] = 0


def read_words(words_list: list, diphthong_dict: dict):
    """
    Load urls from file to 'words_list' and also for each word compute occurrence of diphthongs.
    :param words_list:
    :param diphthong_dict:
    :return: Total number of diphthong occurrences.
    """
    create_diphthongs(diphthong_dict)
    # print(diphthong_dict)
    diphtong_sum = 0
    # with open('words_alpha.txt') as f:
    with open('words.txt') as f:
        for line in f:
            if line == '':
                continue
            word = line.rstrip().lower()
            for key in diphthong_dict.keys():
                num_2 = word.count(key)
                if num_2 > 0:
                    diphthong_dict[key] += (num_2 / float(len(word)))
                    diphtong_sum += num_2
            words_list.append(word)
    f.close()
    return diphtong_sum


def proc_word(word: str, index: int, param_dict: dict):
    """
    Recursive function for creating tree in 'param_dict'.
    Example: input word 'hello':
    h -> e -> l -> l -> o
    d['h'] -> d['h']['e'] - > d['h']['e']['l'] -> d['h']['e']['l']['l'] -> d['h']['e']['l']['l']['o']
    :param word: input word ('facebook.com')
    :param index: index in word
    :param param_dict:
    :return:
    """
    if index > len(word) - 1:
        return
    character = word[index]

    if param_dict.get(character, -1) == -1:
        param_dict[character] = {}
        param_dict[character]['cost'] = 1
    else:
        param_dict[character]['cost'] += 1

    proc_word(word, index + 1, param_dict[character])


def learn_param(words_list: list, param_dict: dict):
    """
    Create tree of characters and for each occurrence of character in the tree add +1 for each word from 'word_list'.
    Example:
        a ...
      /
    a - b ...
      \
        c ...
    Each character has 'cost' property and there is saved value of occorrences.
    :param words_list: list of urls from file.
    :param param_dict: empty dict (so far).
    :return:
    """
    param_dict['cost'] = 0
    largest_word = 0
    for i, word in enumerate(words_list):
        proc_word(word, 0, param_dict)
        if len(word) > largest_word:
            largest_word = len(word)
    print('largest word in the word list: {}'.format(largest_word))


def find_norm_param(param_dict: dict, depth: int, norm_list: list):
    """
    It saves number of occurrences in some level of tree, because all words do not have same length. So appearances of
    character in level N can be different.
    :param param_dict:
    :param depth:
    :param norm_list:
    :return:
    """
    if param_dict.get('cost', -1) == -1:
        return
    norm_list[depth] += param_dict['cost']
    depth += 1
    for key in param_dict.keys():
        if key != 'cost':
            find_norm_param(param_dict[key], depth, norm_list)


def get_norm_list(param_dict: dict, norm_list: list):
    find_norm_param(param_dict, 0, norm_list)


"""
---------- RESTULT --------------
Legit avg:   0.005430646376324761, std: 0.005070732935911104  
Malware avg: 0.0007930775848604364, std: 0.000715665076254574
1750
"""
# def compute_prob(param_dict: dict, norm_list: list, input_word: str):
#     default_cost = 0.01
#     temp_dict = param_dict
#     total_sum = 0
#     index = 0
#     for i, char in enumerate(input_word):
#         index += 1
#         if temp_dict.get(char, -1) != -1:
#             cost = temp_dict[char]['cost']
#             total_sum += (cost / float(norm_list[index]))
#             # total_sum += cost
#             temp_dict = temp_dict[char]
#         else:
#             total_sum = 0.9 * total_sum
#             index = 0
#             # break
#     return total_sum / float(len(input_word))
#     # return total_sum / index
#     # return total_sum


def check_char(temp_dict: dict, char: str, norm_list: list, index: int):
    """
    Take char from word and try if there is occurrence in the tree in such subgraph.
    """
    if temp_dict.get(char, -1) != -1:
        cost = temp_dict[char]['cost']
        com_cost = (cost / float(norm_list[index]))
        return com_cost, True
    return 0, False


def compute_prob(param_dict: dict, norm_list: list, input_word: str):
    """
    Take an input word and compute reward of this word by probabilistic tree model from 'param_dict'.
    If the word is known or is not so weird the reward should be higher.
    :param param_dict:
    :param norm_list:
    :param input_word:
    :return:
    """
    temp_dict = param_dict
    total_sum = 0
    index = 1

    for i, char in enumerate(input_word):
        cost, has_char = check_char(temp_dict, char, norm_list, index)
        if has_char:
            temp_dict = temp_dict[char]
            total_sum += cost
            index += 1
        else:
            total_sum = 0.55 * total_sum

    return total_sum / float(len(input_word))


def normalize_diphtong(diphthong_dict: dict, diphtong_sum: int):
    for key in diphthong_dict.keys():
        diphthong_dict[key] = diphthong_dict[key] / float(diphtong_sum)


def compute_diphthong_occurrence(word: str, diphthong_dict: dict):
    """
    Take input word (url) and
    :param word:
    :param diphthong_dict:
    :return:
    """
    result = 0
    for key in diphthong_dict.keys():
        occ = word.count(key)
        if occ > 0:
            result += occ * diphthong_dict[key]
    return result


def compute_same_consonant(word: str):
    """
    Compute value of tuple consonant in word.
    Exmaple: 'eggs' -> There is tuple of consonant.
    :param word:
    :return:
    """
    is_next_consonant = False
    reward = 0
    for i, char in enumerate(word):
        if char in consonant_list_lower:
            if is_next_consonant:
                reward += 1
            is_next_consonant = True
        else:
            is_next_consonant = False
    return reward / float(len(word))


def compute_same_wovel(word: str):
    """
    Not in usage.
    :param word:
    :return:
    """
    is_next_wovel = False
    reward = 0
    for i, char in enumerate(word):
        if char in wovel_list_lower:
            if is_next_wovel:
                reward += 1
            is_next_wovel = True
        else:
            is_next_wovel = False
    return reward / float(len(word))


def compute_wovel_2(word: str):
    """
    Compute value of wovel and consonant near each other.
    :param word:
    :return:
    """
    reward = 0
    for i, char in enumerate(word):
        if char in wovel_list_lower:
            try:
                t = word[i + 1]
                if t in consonant_list_lower:
                    reward += 1
            except:
                pass
            try:
                t = word[i - 1]
                if t in consonant_list_lower:
                    reward += 1
            except:
                pass
    # return reward
    return reward / float(len(word))


def main():
    """
    Read data, process data, compute features, learn classifier and validate.
    :return:
    """
    words_list = []
    param_dict = {}
    diphthong_dict = {}
    diphtong_sum = read_words(words_list, diphthong_dict)

    print(diphtong_sum)

    learn_param(words_list, param_dict)

    norm_list = [0] * 50
    get_norm_list(param_dict, norm_list)
    # print(sum_list)

    normalize_diphtong(diphthong_dict, diphtong_sum)


    # print('Ready for analyze.')
    # while True:
    #     t = input('Enter word: ')
    #     if len(t) == 0:
    #         continue
    #     res = compute_word(param_dict, sum_list, t)
    #     print('Result: {}'.format(res))

    # Read legit.
    index = 0
    np_array_legit = np.empty([1750])
    np_array_legit_di = np.empty([1750])
    np_array_legit_wovel = np.empty([1750])
    np_array_legit_wovel_2 = np.empty([1750])
    np_array_legit_wovel_3 = np.empty([1750])
    np_array_legit_wordlen = np.empty([1750])
    with open('all_legit.txt') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if line == '':
                continue
            # remove top level domain (.com, .cz, .org, etc.)
            word = remove_top_level_domain(line.lower())
            # word = line.lower()
            np_array_legit[i] = compute_prob(param_dict, norm_list, word)
            np_array_legit_di[i] = compute_diphthong_occurrence(word, diphthong_dict)
            np_array_legit_wovel[i] = compute_wovel_2(word)
            np_array_legit_wovel_2[i] = compute_same_consonant(word)
            # np_array_legit_wovel_3[i] = compute_same_wovel(word)
            np_array_legit_wordlen[i] = len(word)
            index += 1
    f.close()

    np_array_mal = np.empty([1750])
    np_array_mal_di = np.empty([1750])
    np_array_mal_wovel = np.empty([1750])
    np_array_mal_wovel_2 = np.empty([1750])
    np_array_mal_wovel_3 = np.empty([1750])
    np_array_mal_wordlen = np.empty([1750])
    with open('all_malware.txt') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if line == '':
                continue
            # remove top level domain (.com, .cz, .org, etc.)
            word = remove_top_level_domain(line.lower())
            # word = line.lower()
            np_array_mal[i] = compute_prob(param_dict, norm_list, word)
            np_array_mal_di[i] = compute_diphthong_occurrence(word, diphthong_dict)
            np_array_mal_wovel[i] = compute_wovel_2(word)
            np_array_mal_wovel_2[i] = compute_same_consonant(word)
            # np_array_mal_wovel_3[i] = compute_same_wovel(word)
            np_array_mal_wordlen[i] = len(word)
    f.close()

    # print('---------- RESTULT --------------')
    # print('Legit avg:   {}, std: {}  '.format(np.average(np_array_legit), np.std(np_array_legit)))
    # print('Malware avg: {}, std: {}'.format(np.average(np_array_mal), np.std(np_array_mal)))
    # print('Diphthong:')
    # print('Legit avg:   {}, std: {}  '.format(np.average(np_array_legit_di), np.std(np_array_legit_di)))
    # print('Malware avg: {}, std: {}'.format(np.average(np_array_mal_di), np.std(np_array_mal_di)))
    # print('Wovels:')
    # print('Legit avg:   {}, std: {}  '.format(np.average(np_array_legit_wovel), np.std(np_array_legit_wovel)))
    # print('Malware avg: {}, std: {}'.format(np.average(np_array_mal_wovel), np.std(np_array_mal_wovel)))
    print('Words:')
    print('Legit avg:   {}, std: {}  '.format(np.average(np_array_legit_wordlen), np.std(np_array_legit_wordlen)))
    print('Malware avg: {}, std: {}'.format(np.average(np_array_mal_wordlen), np.std(np_array_mal_wordlen)))
    print(index)


    """
    Prepare data for ML algorithms.
    """

    # X1 = np.column_stack((np_array_legit, np_array_legit_di))
    X1 = np.column_stack((np_array_legit, np_array_legit_di, np_array_legit_wordlen,
                          np_array_legit_wovel, np_array_legit_wovel_2, ))
    y1 = np.zeros(1750)

    # X2 = np.column_stack((np_array_mal, np_array_mal_di))
    X2 = np.column_stack((np_array_mal, np_array_mal_di, np_array_mal_wordlen,
                          np_array_mal_wovel, np_array_mal_wovel_2, ))
    y2 = np.ones(1750)

    X = np.concatenate((X1, X2))
    y = np.concatenate((y1, y2))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



    # ADABOOST
    # Accuracy2: 0.8342857142857143
    # Accuracy3: 0.8523809523809524
    # Accuracy4: 0.8809523809523809 np_array_legit, np_array_legit_di, np_array_legit_wordlen, np_array_legit_wovel, np_array_legit_wovel_2
    print('---- ADABOOST -----')
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=3),
                             algorithm="SAMME",
                             n_estimators=200)
    bdt.fit(X_train, y_train)
    y_predicted = bdt.predict(X_test)


    # # Random forest
    # # Accuracy2: 0.8114285714285714
    # # Accuracy3: 0.8371428571428572
    # # Accuracy4: 0.8514285714285714 Accuracy4: 0.861904761904762 Accuracy: 0.8723809523809524
    # # Accuracy5 0.878095238095238 -np_array_legit, np_array_legit_di, np_array_legit_wordlen, np_array_legit_wovel, np_array_legit_wovel_2
    # print('Random forest')
    # model = RandomForestClassifier(n_estimators=100, oob_score='TRUE')
    # model.fit(X_train, y_train)
    # y_predicted = model.predict(X_test)



    # # SVM
    # # Accuracy2: 0.49
    # # Accuracy3: 0.7228571428571429
    # # Accuracy4: 0.7790476190476191
    # # Accuracy 0.7980952380952381
    # print('---- SVM -----')
    # clf = svm.SVC()
    # clf.fit(X_train, y_train)
    # y_predicted = clf.predict(X_test)


    # # XGBOOST
    # # Accuracy2: 0.819047619047619
    # # Accuracy3: 0.8361904761904762
    # # Accuracy4: 0.839047619047619
    # # Accuracy4: 0.8552380952380952
    # # Accuracy 0.8666666666666667
    # print('------ XGBOOST --------')
    # model = XGBClassifier(
    #     learning_rate=0.1,
    #     n_estimators=1000,
    #     max_depth=3,
    #     min_child_weight=5,
    #     gamma=0.1,
    #     subsample=0.8,
    #     colsample_bytree=0.8,
    #     objective='binary:logistic',
    #     nthread=4,
    #     scale_pos_weight=1,
    #     seed=27)
    # model.fit(X_train, y_train)
    # y_predicted = model.predict(X_test)




    acc = accuracy_score(y_test, y_predicted)
    con_matrix = confusion_matrix(y_test, y_predicted)
    print('Accuracy: {}'.format(acc))
    print('False positive rate: {}'.format(con_matrix[0][1] / float(con_matrix[0][1] + con_matrix[1][1])))

    print(classification_report(y_test, y_predicted))


    # # Plot
    # plt.plot(np_array_legit, np_array_legit_di, 'ro')
    # plt.plot(np_array_mal, np_array_mal_di, 'bo')
    # plt.axis([0, np.max(np_array_legit), 0, np.max(np_array_legit_di)])
    # plt.show()


if __name__ == '__main__':
    main()
    # main_2()
