# coding: utf-8
from __future__ import division
from MentionDetection.MentionDetection_by_parse import Mention_Detection
import LoadConll
from sklearn.metrics import classification_report
import numpy as np


def __get_mention_idx(obj_document):
    """
    获取obj_document中 lst Mention的token下标
    :return: [(1,2),(3,4)]
    """
    result = []
    for mention in obj_document.lst_mentions:
        result.append((mention.lst_tokens[0].token_id,
                       mention.lst_tokens[-1].token_id))
    return result

def count_md_prf(obj_gold_data, obj_result_data):
    """
    假设一共有10篇文章，里面4篇是你要找的。
    根据你某个算法，你认为其中有5篇是你要找的，但是实际上在这5篇里面，只有3篇是真正你要找的。
    那么你的这个算法的precision是3/5=60%，也就是，你找的这5篇，有3篇是真正对的
    这个算法的recall是3/4=75%，也就是，一共有用的这4篇里面，你找到了其中三篇。
    """
    gold_data = __get_mention_idx(obj_gold_data)
    result_data = __get_mention_idx(obj_result_data)

    # print gold_data
    # print result_data

    set_right = set(gold_data)
    set_auto = set(result_data)
    try:
        precision = len(set_right.intersection(set_auto)) / len(set_auto)
        recall = len(set_right.intersection(set_auto)) / len(set_right)
        f_score = (precision * recall * 2) / (precision + recall)
    except ZeroDivisionError:
        return (0, 0, 0)

    return (precision, recall, f_score)

def main(file_):
    # 用于计算prf
    # md_gold_data = LoadConll.load_one_file(file_)
    # 其实md_org_data 和 md_res_data的id一样
    md_org_data = LoadConll.load_one_file_for_md(file_)
    md_res_data = Mention_Detection(md_org_data)
    # print count_md_prf(md_gold_data, md_res_data)
    return md_res_data

    # return count_md_prf(md_gold_data, md_res_data)


if __name__ == '__main__':
    # test = 'test.v4_gold_conll'
    test = '/opt/tmp/DataSets/conll_test/test/cts_0039_000.v4_gold_conll'
    # 用于计算prf
    md_gold_data = LoadConll.load_one_file(test)
    # 其实md_org_data 和 md_res_data的id一样
    md_org_data = LoadConll.load_one_file_for_md(test)
    md_res_data = Mention_Detection(md_org_data)
    print count_md_prf(md_gold_data, md_res_data)
    print 'shit'
    print md_org_data == md_res_data
    for m in md_org_data.lst_mentions:
        print m.chinese_word, m.mention_id