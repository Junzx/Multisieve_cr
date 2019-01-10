# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from time import clock
from LoadConll import load_one_file
from SubjectUtils.sieve_utils import get_modifier
from Multisieve.pronounce_cr import pronoun_sieve
from Multisieve.test_sieve import test_sieve
from Multisieve.exact_match import exact_match
from Multisieve.precise_constructs import precise_constructs
from Multisieve.strict_head_matching_A import strict_head_matching_A
from Multisieve.strict_head_matching_B import strict_head_matching_B
from Multisieve.strict_head_matching_C import strict_head_matching_C

import SubjectUtils.unit_test_utils as unit_test_utils

import logging
logging.basicConfig(filename="load_data.log",
                    level=logging.INFO)
logger = logging.getLogger("experiments")

def __test(file_):
    document_object = load_one_file(file_)
    for mention in document_object.lst_mentions:
        obj_sent = document_object.dic_sentences.get(mention.sent_id)
        print mention.chinese_word, "|", obj_sent.get_sent()
        mod_ = get_modifier(obj_sent, mention)
        print mod_
        print

def main(file_):
    start = clock()
    document_object = load_one_file(file_)
    logger.info("加载数据用时： %f"%(clock() - start))
    sieve_order = [
        test_sieve,
        # exact_match,
        # precise_constructs,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        # pronoun_sieve,
    ]
    logger.info("开始调用multi-sieve")
    for sieve in sieve_order:
        print sieve
        logger.info("Run " + str(sieve))
        sieve_start = clock()
        document_object = sieve(document_object)
        sieve_end = clock()
        logger.info("%s用时：%f"%(str(sieve), sieve_end - sieve_start))
        # unit_test_utils.print_cluster(document_object)
        print '-' * 30
    print ''
    logger.info("总用时：%f"%(clock() - start))
    # unit_test_utils.print_gold_cluster(document_object)
    unit_test_utils.print_cluster(document_object)



if __name__ == '__main__':
    # test_file = 'small_test2.conll'
    test_file = 'test.v4_gold_conll'
    main(test_file)
    # __test(test_file)