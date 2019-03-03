# -*- coding: UTF-8 -*-
"""
获取各类词表，返回的是unicode的list

新的
"""
from ConstantVariable import corpus_dict

def get_quantifier():
    return corpus_dict.get('quantifier')

def get_nation():
    return corpus_dict.get('nation')

def get_adj_nation():
    return corpus_dict.get('adj_nation')

def get_stop_words():
    return corpus_dict.get('stop_word')

def get_report_verbs():
    return corpus_dict.get('report_verbs')

def get_determiner_words():
    return corpus_dict.get('determiner_word')

def get_conjunction_words():
    return corpus_dict.get('conjunction_word')

def get_verbs():
    return corpus_dict.get('verb')

def get_animals():
    return corpus_dict.get('animal')

def get_botanical():
    return corpus_dict.get('botanical')

def get_synonym_words():
    return corpus_dict.get('synonym_word')

def get_pca_list():
    return corpus_dict.get('pca_list')

def get_abbreviation_dict():
    return corpus_dict.get('abbreviation_dict')