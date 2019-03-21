# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from time import clock
# from cPickle import load, dump
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
import config_sieve_order

import logging

logging.basicConfig(filename=config.project_path + "/RunResults/MyLog.log",
                    level=logging.INFO, filemode='w')
logger = logging.getLogger("Coreference_Sieves_Order")

sieve_order = config_sieve_order.sieve_order


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
# sieve_order = [
#         test_sieve,
#         exact_match,
#         strict_head_matching_A,
#         strict_head_matching_B,
#         strict_head_matching_C,
#         proper_header_word_match_sieve,
#         # precise_constructs,
#         # relaxing_head_matching,
#         discourse_processing,
#         pronoun_sieve,
#         other_sieve,
#         filter_sieve,
#     ]

# # 按照Precision降序
# sieve_order = [
        # test_sieve,
        # exact_match,
        # strict_head_matching_A,
        # strict_head_matching_B,
        # strict_head_matching_C,
        # proper_header_word_match_sieve,
        # pronoun_sieve,
        # discourse_processing,
        # precise_constructs,
        # relaxing_head_matching,
        # other_sieve,
        # filter_sieve,
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
#     filter_sieve,
# ]



def main(file_):
    """
    新函数，只进行multi sieve，并写入文件
    UPDATE: 根据传入的file_判断是文件路径还是document object
    """
    start = clock()
    if isinstance(file_, str):
        document_object = load_one_file(file_)
    else:
        document_object = file_
    # logger.info("---------开始调用multi-sieve---------\n")
    for sieve in sieve_order:
        pprint(sieve)
        document_object = sieve(document_object)
        logger.info("Run %s\n" % str(sieve))



    # 想好要不要写入文件！
    result_file_path = config.result_folder + document_object.document_file_name + '.v4_result_conll'
    document_object.write_to_file(result_file_path)
    logger.info("-------处理完毕，结果写入 %s-------\n\n"%result_file_path)

    # unit_test_utils.print_cluster(document_object)
    # unit_test_utils.print_gold_cluster(document_object)

    return document_object


def __unit_test(file_):
    document_object = load_one_file(file_)
    # document_object = discourse_processing(document_object)
    document_object = other_sieve(document_object)
    # pprint(write_log_prf(document_object))




if __name__ == '__main__':
    test_file = 'small_test2.conll'
    # test_file = 'test.v4_gold_conll'
    test_file_2 = '/opt/tmp/DataSets/conll_test/test/chtb_0249_000.v4_gold_conll'

    res = main(test_file_2)
    # unit_test_utils.print_cluster(res)
    # unit_test_utils.print_gold_cluster(res)

    # __test(test_file)