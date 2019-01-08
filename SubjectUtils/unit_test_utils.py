# -*- coding: UTF-8 -*-
"""
测试用的函数，包括打印输出、测试prf，写入文件等
"""
from sys import version
def print_str(string):
    """
    打印输出的函数，统一按照python2的写法调用即可
    :param string:
    :return:
    """
    if version.startswith('2'):
        print string
    elif version.startswith('3'):
        print(string)


def get_prf(obj_document):
    pass


def __mention_2_entity(obj_document, var='gold'):
    """
    遍历所有的mention，构建entity
    """
    dic = {}
    for mention in obj_document.lst_mentions:
        if var == 'auto':
            entity_id = mention.entity_id
        elif var == 'gold':
            entity_id = mention.gold_entity_id

        if entity_id not in dic:
            dic.setdefault(entity_id, [])
        dic[entity_id].append(mention)
    return dic

def print_gold_cluster(obj_document):
    """
    输出这个document的标准答案
    针对gold_mentions
    """
    print_str('标准答案（from file）：')
    dic = __mention_2_entity(obj_document, var='gold')
    for entity_id, mention_list in dic.items():
        print_str('Entity_id: (' + str(entity_id) + ') ,')
        for m in mention_list:
            print_str("词： %s | mention id: %d" %(m.chinese_word, m.mention_id))


def print_cluster(obj_document):
    """
    输出entity
    """
    print_str('当前聚类情况：')
    dic = __mention_2_entity(obj_document, var='auto')
    for entity_id, mention_list in dic.items():
        if len(mention_list) > 1:
            print_str('Entity_id: (' + str(entity_id) + ') ')
            for m in mention_list:
                print_str("词： %s | mention id: %d"%(m.chinese_word, m.mention_id))

