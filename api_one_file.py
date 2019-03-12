# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from time import clock
from cPickle import load, dump
from LoadConll import load_one_file
from pprint import pprint

from SubjectUtils.sieve_utils import get_modifier

# ---------- 7 pass -------------
from Multisieve.test_sieve import test_sieve
from Multisieve.exact_match import exact_match
from Multisieve.precise_constructs import precise_constructs
from Multisieve.strict_head_matching_A import strict_head_matching_A
from Multisieve.strict_head_matching_B import strict_head_matching_B
from Multisieve.strict_head_matching_C import strict_head_matching_C
from Multisieve.relaxing_head_matching import relaxing_head_matching
from Multisieve.pronounce_cr import pronoun_sieve
# ------
from Multisieve.discourse_processing import discourse_processing
from Multisieve.proper_head_word_match import proper_header_word_match_sieve
from Multisieve.other_sieve import other_sieve
from Multisieve.final_sieve import filter_sieve
# -------------------------------


import SubjectUtils.unit_test_utils as unit_test_utils
import SubjectUtils.sieve_utils as sieve_utils
import SubjectUtils.experiment_utils as experiment_utils
import config

import logging

logging.basicConfig(filename=config.project_path + "/RunResults/MyLog.log",
                    level=logging.INFO, filemode='w')
logger = logging.getLogger("experiments")



# 原始顺序
# sieve_order = [
        # test_sieve,
        # exact_match,
        # precise_constructs,
        # strict_head_matching_A,
        # strict_head_matching_B,
        # strict_head_matching_C,
        # relaxing_head_matching,
        # pronoun_sieve,
        # proper_header_word_match_sieve,
        # discourse_processing,
        # other_sieve,
        # filter_sieve,
    # ]


# 我的顺序
sieve_order = [
        test_sieve,
        # exact_match,
        # strict_head_matching_A,
        # strict_head_matching_B,
        # strict_head_matching_C,
        proper_header_word_match_sieve,
        # precise_constructs,
        # relaxing_head_matching,
        # discourse_processing,
        # pronoun_sieve,
        # other_sieve,
        # filter_sieve,
    ]

# # 按照Precision降序
# sieve_order = [
#         test_sieve,
#         exact_match,
#         strict_head_matching_A,
#         strict_head_matching_B,
#         strict_head_matching_C,
#         proper_header_word_match_sieve,
#         pronoun_sieve,
#         discourse_processing,
#         precise_constructs,
#         relaxing_head_matching,
#         other_sieve,
#         filter_sieve,
# ]

# 按照Recall升序
# sieve_order = [
#     discourse_processing,
#     exact_match,
#     pronoun_sieve,
#     precise_constructs,
#     strict_head_matching_A,
#     strict_head_matching_C,
#     other_sieve,
#     strict_head_matching_B,
#     proper_header_word_match_sieve,
#     relaxing_head_matching,
# ]



# sieve_order = [
#     exact_match
# ]



def __test(file_):
    document_object = load_one_file(file_)
    # document_object = discourse_processing(document_object)
    document_object = other_sieve(document_object)
    # pprint(write_log_prf(document_object))


def main_old(file_):
    """
    update： 2019-2-24
    弃用此函数，不在运行的时候评价
    """
    start = clock()
    if isinstance(file_, unicode):
        document_object = load_one_file(file_)
    else:
        document_object = file_
    logger.info("加载数据用时： %f"%(clock() - start))

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

        # 以下是对每个sieve计算一次prf
        # sieve_prf = experiment_utils.get_document_prf(document_object)  # 计算prf
        # all_result['order_list'].append(sieve.__name__)
        # all_result['muc'].append(sieve_prf['muc'])
        # all_result['ceafe'].append(sieve_prf['ceafe'])
        # all_result['ceafm'].append(sieve_prf['ceafm'])
        # all_result['blanc'].append(sieve_prf['blanc'])
        # all_result['bcub'].append(sieve_prf['bcub'])

        sieve_end = clock()
        logger.info("%s用时：%f"%(str(sieve), sieve_end - sieve_start))
        # unit_test_utils.print_cluster(document_object)
        # print '-' * 30
    file_prf = experiment_utils.get_document_prf(document_object)
    logger.info("总用时：%f"%(clock() - start))

    return file_prf

def main(file_):
    """
    新函数，只进行multisieve，并写入
    """
    start = clock()
    if isinstance(file_, str):
        document_object = load_one_file(file_)
    else:
        document_object = file_
    logger.info("加载数据用时： %f" % (clock() - start))
    logger.info("开始调用multi-sieve")
    for sieve in sieve_order:
        print sieve
        logger.info("Run " + str(sieve))
        sieve_start = clock()
        document_object = sieve(document_object)
        sieve_end = clock()
        logger.info("%s用时：%f" % (str(sieve), sieve_end - sieve_start))

    # 然后写入文件
    result_file_path = config.result_folder + document_object.document_file_name + '.v4_result_conll'
    document_object.write_to_file(result_file_path)
    # unit_test_utils.print_gold_cluster(document_object)
    return document_object

if __name__ == '__main__':
    test_file = 'small_test2.conll'
    # test_file = 'test.v4_gold_conll'
    test_file_2 = '/opt/tmp/DataSets/conll_test/test/cctv_0007_003.v4_gold_conll'

    res = main(test_file_2)
    print res

    # __test(test_file)

    # res_dic = load(open('./RunResults/Scorer_prf.dict', 'rb'))
    # plot_result(res_dic)