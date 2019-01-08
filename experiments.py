# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from LoadConll import load_one_file
from Multisieve.pronounce_cr import pronoun_sieve
from Multisieve.test_sieve import test_sieve
from Multisieve.exact_match import exact_match
from Multisieve.precise_constructs import precise_constructs

import SubjectUtils.unit_test_utils as unit_test_utils

import logging
logging.basicConfig(filename="load_data.log",
                    level=logging.INFO)
logger = logging.getLogger("experiments")

def main(file_):
    document_object = load_one_file(file_)
    sieve_order = [
        # pronoun_sieve,
        test_sieve,
        precise_constructs,
        # exact_match,
    ]
    logger.info("开始调用multi-sieve")
    for sieve in sieve_order:
        logger.info("Run " + str(sieve))
        document_object = sieve(document_object)
        # unit_test_utils.print_gold_cluster(document_object)
        # unit_test_utils.print_cluster(document_object)
        print '-' * 30
    print ''


if __name__ == '__main__':
    test_file = 'small_test2.conll'
    # test_file = 'test.v4_gold_conll'
    main(test_file)