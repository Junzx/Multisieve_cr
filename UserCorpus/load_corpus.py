# -*- coding: UTF-8 -*-
"""
获取各类词表，返回的是unicode的list
"""
import json
import config
from os import getcwd
import logging

logger = logging.getLogger("Corpus_Loader")

corpus_path = config.project_path + '/UserCorpus/Corpus/'
EOF = '\n'

def format_words(func):
    """
    装饰器，用来格式化最终的返回值
    """
    def format_():
        lst = func()
        tmp = [i.decode('utf-8') for i in lst]
        return tuple([i.strip('\n').strip('\r\n').strip('\r') for i in tmp])
    return format_



# 带下划线的私有变量是读取那啥的

@format_words
def get_quantifier():
    """
    :return:量词list
    """
    lst_tmp = []
    with open(corpus_path + 'quantifier.txt', 'r') as file_handle:
        quantifier_init = file_handle.read()
        for str_iter_quantifier in quantifier_init.split('\t'):
            lst_tmp.append(str_iter_quantifier.split()[-1].strip(' '))  # 有的量词前面有莫名其妙的字符 处理一下
    return lst_tmp



@format_words
def get_nation():
    """
    :return:国家名称list，如America
    """
    lst_tmp = []
    with open(corpus_path + 'nations.txt', 'r') as file_handle:
        adj_nations_init = file_handle.read()
        for i in adj_nations_init.split(EOF):
            if len(i.split()) != 0:  # 可能有空行
                lst_tmp.append(i.split()[0])  # 第一列是国家名
    return lst_tmp

# @format_words
def get_adj_nation():
    return [i + u'人' for i in get_nation()]

@format_words
def get_stop_words():
    """
    :return: 停用词list，中文
    """
    with open(corpus_path + 'stopwords.txt', 'r') as file_handle:
        stopwords_init = file_handle.read()
        return stopwords_init.split(EOF)

def get_report_verbs():
    """
    :return:表示表达的动词list，中文
    """
    with open(corpus_path + 'reportverb.txt', 'r') as file_handle:
        return file_handle.read().split(EOF)

@format_words
def get_determiner_words():
    """
    :return:表示限定词的list，中文
    """
    with open(corpus_path + 'det.txt', 'r') as file_handle:
        return file_handle.read().split(EOF)

@format_words
def get_conjunction_words():
    """
    :return: 连词 list，中文
    """
    with open(corpus_path+'conj.txt','r') as file_handle:
        return file_handle.read().split(EOF)

@format_words
def get_verbs():
    """
    :return: 动词
    """
    with open(corpus_path + 'verbs.txt','r') as file_handle:
        return file_handle.read().split('\n')

@format_words
def get_animals():
    """
    动物词典
    :return:
    """
    with open(corpus_path + 'animals.txt', 'r') as file_handle:
        return file_handle.read().split('\n')

@format_words
def get_botanical():
    """
    植物词典
    :return:
    """
    with open(corpus_path + 'botanical.txt', 'r') as file_handle:
        return file_handle.read().split('\n')

def get_synonym_words():
    """
    这个不能用装饰器
    用哈工大同义词林那个，等号表示同义词，最后返回一个tup套tup的形式
    """
    with open(corpus_path + 'synonym.txt','r') as file_handle:
        lst_synonym = []
        for line in file_handle:

            # 只处理同义词，否则就跳过
            if '=' not in line:
                continue
            line = line.strip('\n')
            lst_synonym.append(tuple([i.decode('utf-8') for i in line.strip('\r').split(' ')[1:]]))
    return lst_synonym

def get_pca_list():
    """
    "北京市": {
        "市辖区": [
            "东城区",
            "西城区",
            .....
        ]
    },
    :return: 所有区的名字，如：(北京市、北京、海淀区、海淀)
    """
    with open(corpus_path + 'pca.json', 'r') as hdl:
        data = json.load(hdl)

    city_list = []
    for shi, qu in data.items():
        if isinstance(qu, dict):
            for qu_ming, qu_list in qu.items():
                city_list.extend(qu_list)
        elif isinstance(qu, list):
            city_list.extend(qu)
    filter_ = lambda x: x.strip(u'区').strip(u'县').strip(u'市').strip(u'省')
    tmp = map(filter_, city_list)
    city_list.extend(tmp)
    return tuple(set(city_list))

def get_abbreviation_dict():
    """
    缩写的字典
    :return:
    """
    with open(corpus_path + 'abbreviation.json', 'r') as hdl:
        return json.load(hdl)


# all_corpus_dict = {
#     'quantifier': __get_quantifier(),
# }



if __name__ == '__main__':
    from pprint import pprint
    corpus_path = './Corpus/'
    print get_abbreviation_dict()
    # print get_determiner_words()
    # for i in get_nation():
    #     print i
    # print get_quantifier()
    # print get_stop_words()
    # print get_conjunction_words()
    # res = get_pca_list()[:100]
    # for i in res:
    #     print i
    # print res[1]
    # print
    # print len(get_pca_list())
    # with open(corpus_path + 'abbreviation-1.txt', 'r') as hdl:
    #     dic_ = {}
    #     for line in hdl:
    #         if line.startswith('n'):
    #             continue
    #         line = line.decode('utf-8')
    #         part1, part2 = line.split(':')
    #         tmp = part2.split(' ')
    #         tmpp = [i.split('/')[0] for i in tmp]
    #         long_words = ''.join(tmpp)
    #         dic_.setdefault(part1, long_words)
    #
    # with open(corpus_path + 'abbreviation.json', 'w+') as json_hdl:
    #     json.dump(dic_, json_hdl)