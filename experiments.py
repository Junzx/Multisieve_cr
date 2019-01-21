# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from time import clock
from cPickle import load, dump
from shutil import copyfile
from LoadConll import load_one_file
from os import remove, getcwd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

from SubjectUtils.sieve_utils import get_modifier

from Multisieve.test_sieve import test_sieve
from Multisieve.exact_match import exact_match
from Multisieve.precise_constructs import precise_constructs
from Multisieve.strict_head_matching_A import strict_head_matching_A
from Multisieve.strict_head_matching_B import strict_head_matching_B
from Multisieve.strict_head_matching_C import strict_head_matching_C
from Multisieve.relaxing_head_matching import relaxing_head_matching
from Multisieve.pronounce_cr import pronoun_sieve

import SubjectUtils.unit_test_utils as unit_test_utils
import SubjectUtils.sieve_utils as sieve_utils
import Scorer.api_prf


import logging
logging.basicConfig(filename="./RunResults/MyLog.log",
                    level=logging.INFO)
logger = logging.getLogger("experiments")

def __test(file_):
    document_object = load_one_file(file_)
    document_object.write_to_file()
    # unit_test_utils.print_gold_cluster(document_object)
    # for mention in document_object.lst_mentions:
    #     print '---------------'
    #     print mention.mention_id, mention.chinese_word
    #     candidate_ = sieve_utils.get_candidate_mentions(document_object, mention)
    #     print len(candidate_)
    #     for c in candidate_:
    #         print c.chinese_word, c.mention_id, '|',
    #     print


        # obj_sent = document_object.dic_sentences.get(mention.sent_id)
        # print mention.chinese_word, "|", obj_sent.get_sent()
        # mod_ = get_modifier(obj_sent, mention)
        # print mod_
        # print
    a = document_object
    print a.__dict__

def write_log_prf(obj_document):
    document_prf = {
        'muc': None,
        'blanc': None,
        'ceafe': None,
        'ceafm': None,
        'bcub': None,
    }
    # gold_file
    gold_file = obj_document.original_document_path
    # result file
    res_file = obj_document.result_document_path
    # 写入tmp文件
    obj_document.write_to_file(res_file)

    # 目的路径
    target_folder = getcwd() + '/Scorer/'
    gold_target_file = target_folder + gold_file
    result_target_file = target_folder + res_file

    # 复制文件
    copyfile(gold_file, gold_target_file)
    copyfile(res_file, result_target_file)

    # 调用perl
    res_muc = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "muc")
    res_blanc = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "blanc")
    res_ceafe = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "ceafe")
    res_ceafm = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "ceafm")
    res_bcub = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "bcub")

    # 删除复制过去的文件
    remove(gold_target_file)
    remove(result_target_file)

    # 删除那啥
    remove(res_file)

    document_prf['muc'] = np.array(res_muc)
    document_prf['blanc'] = np.array(res_blanc)
    document_prf['ceafe'] = np.array(res_ceafe)
    document_prf['ceafm'] = np.array(res_ceafm)
    document_prf['bcub'] = np.array(res_bcub)

    return document_prf

def plot_result(res_dict):
    """
    这个函数用来画图，回应称
    :param res_dict:
    :return:
    """
    def __precent_2_float(str_):
        return float(str_.strip('%')) * 0.01

    # with open('./RunResults/Scorer_prf.dict', 'wb') as hdl:
    #     dump(res_dict, hdl)

    sieve_order = res_dict.get('order_list')

    for score_name, scores in res_dict.items():
        if score_name == 'order_list':
            continue

        # 转换为array
        scores = np.array(scores)
        p_ = map(__precent_2_float, scores[:, 0])
        r_ = map(__precent_2_float, scores[:, 1])
        f_ = map(__precent_2_float, scores[:, 2])

        mpl.rcParams['font.sans-serif'] = ['SimHei']
        plt.figure(figsize=(20, 10))
        x = sieve_order

        plt.plot(x,p_,marker='o',label = u'Precision')
        plt.plot(x,r_,marker = '*', label = u'Recall')
        plt.plot(x,f_,marker = '^',label = u'F_score')
        plt.legend()    # 让图例生效

        plt.xlabel(u"Sieves") #X轴标签
        plt.ylabel(u"Values") #Y轴标签
        plt.title(u"Matrix of " + score_name + u" | PRF of Each Sieves")
        # ax = axes()
        # ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.savefig('./RunResults/' + score_name + '.png')
        plt.close()

def main(file_):
    print 'Main!'
    start = clock()
    document_object = load_one_file(file_)
    logger.info("加载数据用时： %f"%(clock() - start))
    sieve_order = [
        test_sieve,
        exact_match,
        precise_constructs,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        relaxing_head_matching,
        pronoun_sieve,
    ]
    all_result = {
        'muc': [],
        'bcub': [],
        'ceafe': [],
        'ceafm': [],
        'blanc': [],
        'order_list': []
    }
    logger.info("开始调用multi-sieve")
    for sieve in sieve_order:
        print sieve
        logger.info("Run " + str(sieve))
        sieve_start = clock()
        document_object = sieve(document_object)

        sieve_prf = write_log_prf(document_object)  # 计算prf
        all_result['order_list'].append(sieve.__name__)
        all_result['muc'].append(sieve_prf['muc'])
        all_result['ceafe'].append(sieve_prf['ceafe'])
        all_result['ceafm'].append(sieve_prf['ceafm'])
        all_result['blanc'].append(sieve_prf['blanc'])
        all_result['bcub'].append(sieve_prf['bcub'])

        sieve_end = clock()
        logger.info("%s用时：%f"%(str(sieve), sieve_end - sieve_start))
        # unit_test_utils.print_cluster(document_object)
        print '-' * 30

    plot_result(all_result) # 画图

    print ''
    logger.info("总用时：%f"%(clock() - start))
    # unit_test_utils.print_gold_cluster(document_object)
    # print '-=' * 20
    # unit_test_utils.print_cluster(document_object)

    # document_object.write_to_file("test.v4_res_conll")


if __name__ == '__main__':
    # test_file = 'small_test2.conll'
    # test_file = 'test.v4_gold_conll'
    # main(test_file)
    # __test(test_file)
    res_dic = load(open('./RunResults/Scorer_prf.dict', 'rb'))
    plot_result(res_dic)