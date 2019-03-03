# coding:utf-8
"""
负责mention detection的部分，读取conll，形成source.txt & target.txt

"""

import config
import os
import LoadConll
from math import fabs

# file_list = config.get_var_files(config.gold_test)
# source_txt = open('test_source.txt', 'w')
# target_txt = open('test_target.txt', 'w')


file_list = config.get_var_files(config.gold_train)
source_txt = open('train_source.txt', 'w')
target_txt = open('train_target.txt', 'w')


def conll2txt(file_):
    print file_
    obj_data = LoadConll.load_one_file(file_)
    for sent_id, sent_obj in obj_data.dic_sentences.items():
        word_list = []
        label_list = []
        _tmp_label = 'O'
        flag_jump = False
        for token in sent_obj.lst_tokens:
            if token.word_itself == 'ＥＭＰＴＹ':
                flag_jump = True
                continue
            if token.np_info == '-':
                _tmp_label = 'O'
            else:
                _tmp_label = 'B'

            # elif token.np_info != '-' and _tmp_label == 'O':
            #     _tmp_label = 'B'
            # elif token.np_info != '-' and _tmp_label == 'B':
            #     _tmp_label = 'I'

            word_list.append(token.word_itself)
            label_list.append(_tmp_label)
        if not flag_jump:
            source_txt.write(' '.join(word_list) + '\n')
            target_txt.write(' '.join(label_list) + '\n')

def conll2txt_new(file_):
    data = LoadConll.load_one_file(file_)

    lst_mention_id = []
    for mention in data.lst_mentions:
        _tmp = (mention.lst_tokens[0].token_id, mention.lst_tokens[-1].token_id)
        lst_mention_id.append(_tmp)

    hash_map = {}
    for tmp in lst_mention_id:
        if tmp[0] not in hash_map:
            hash_map.setdefault(tmp[0], tmp)
        elif tmp[0] in hash_map:
            shit = hash_map[tmp[0]]
            if tmp[1] > shit[1]:
                hash_map.setdefault(tmp[0], tmp)
            else:
                continue

    # 删去重叠的，保留短的
    # 如果长度相同，保留后面的
    hash_map_new = {}
    last_item = [-1, -1]    # 初始化
    for hash_id, item in hash_map.items():
        if hash_id in range(last_item[0], last_item[1] + 1):
            if fabs(last_item[0] - last_item[1]) > fabs(item[0] - item[1]) or \
                   item[1] > last_item[1]:
                del hash_map_new[last_item[0]]  #
            elif item[1] <= last_item[1]:
                continue
        hash_map_new.setdefault(hash_id, item)

        last_item = item

    # 然后统一执行写入
    source_list = []
    target_list = []
    jump = -1
    for token in data.lst_tokens:
        source_list.append(token.word_itself)
        if token.token_id in hash_map_new:
            shit = hash_map_new.get(token.token_id)
            jump = shit[1]
            target_list.append('B')
            continue

        if token.token_id <= jump:
            target_list.append('I')
            continue
        target_list.append('O')


    if len(source_list) == len(target_list):
        source_txt.write(' '.join(source_list) + '\n')
        target_txt.write(' '.join(target_list) + '\n')




if __name__ == '__main__':
    test_ = 'test.v4_gold_conll'
    # conll2txt(test_)

    # conll2txt_new(test_)

    #
    for file_ in file_list:
        print file_
        conll2txt_new(file_)

