# coding:utf-8
import config
import os
import LoadConll
import cPickle
import numpy as np

def conll2sent(file_):
    obj_data = LoadConll.load_one_file(file_)
    token_list = []
    label_list = []
    for sent_id, sent in obj_data.dic_sentences.items():
        tmp_token = []
        tmp_label = []
        label_token = [token for mention in sent.lst_mentions for token in mention.lst_tokens]
        for token in sent.lst_tokens:
            tmp_token.append(token.word_itself)
            if token in label_token:
                tmp_label.append('T')
            else:
                tmp_label.append('F')
        token_list.append(np.asarray(tmp_token))
        label_list.append(np.asarray(tmp_label))
    return token_list, label_list

if __name__ == '__main__':
    # print os.listdir(config.basic_folder + config.gold_train)
    test_ = 'test.v4_gold_conll'
    #
    # tokens, labels = conll2sent(test_)
    # print labels
    # raise MemoryError
    # for i in range(len(tokens)):
    #     assert len(tokens[i]) == len(labels[i])
    #     print '---------------'
    #     for j in range(len(tokens[i])):
    #         print tokens[i][j], labels[i][j]

    all_token = []
    all_label = []
    # folder = config.basic_folder + config.gold_train
    folder = config.basic_folder + config.gold_test
    for f in os.listdir(folder):#[:2]:
        if 'gold' not in f:
            continue
        file_ = folder + f
        print file_
        token, label = conll2sent(file_)
        all_token.extend(token)
        all_label.extend(label)
    with open('test.token', 'wb') as hdl:
        cPickle.dump(np.asarray(all_token), hdl)
    with open('test.label', 'wb') as hdl:
        cPickle.dump(np.asarray(all_label), hdl)
    # from pprint import pprint



