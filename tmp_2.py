# coding:utf-8
"""
负责mention detection的部分，读取conll，形成source.txt & target.txt

"""

import config
import os
import LoadConll

file_list = config.get_var_files(config.gold_test)

source_txt = open('test_source.txt', 'w')
target_txt = open('test_target.txt', 'w')

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


if __name__ == '__main__':
    # test_ = 'test.v4_gold_conll'
    # conll2txt(test_)

    for file_ in file_list:#[:5]:
        conll2txt(file_)

