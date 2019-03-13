# coding: utf-8
from time import clock
import config
import cPickle

import numpy as np

def load_emb(emb_path):
    start = clock()
    dic = {}
    with open(emb_path, 'rb') as hdl:
        emb = hdl.readlines()
    for i in emb:
        lst_i = i.strip('\n').split(' ')[:-1]
        emb = np.array([float(i) for i in lst_i[1:]])
        # dic.setdefault(lst_i[0].decode('utf-8'), emb)
        dic.setdefault(lst_i[0], emb)
    print 'load embedding success! use time: ', clock() - start
    return dic

char_emb = load_emb(config.embedding_path)
char_emb_dim = config.embedding_dim

def get_char_emb(char_str):
    #return char_emb.get(char_str, np.random.rand(char_emb_dim))
    return char_emb.get(char_str, np.random.randn(1,char_emb_dim))

def load_file(f_):
    with open(f_, 'r') as hdl:
        return map(lambda s:s.strip('\n').decode('utf-8'), hdl.readlines())


def make_metrix(lst_word_list):
    word_metrix = []
    for word in lst_word_list:
        word_vector = []
        for char in word:
            tmp_ = get_char_emb(char)
            word_vector.extend(tmp_)

        if len(word_vector) >= 300 * 30:
            word_metrix.append(word_vector[:9000])
        else:
            tmp = []
            tmp.extend(list(word_vector))
            tmp.extend([0 for _ in range(9000 - len(word_vector))])
            word_metrix.append(np.array(tmp))
    return np.array(word_metrix)

def load_model(model_path):
    with open(model_path, 'rb') as hdl:
        return cPickle.load(hdl)

def save_model(model_path, object_):
    with open(model_path, 'wb') as hdl:
        cPickle.dump(hdl, object_)
