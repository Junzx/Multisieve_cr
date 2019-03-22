# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from time import clock
# from cPickle import load, dump
from LoadConll import load_one_file
from pprint import pprint

from SubjectUtils.sieve_utils import get_modifier

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


def main(file_):
    """
    新函数，只进行multi sieve，并写入文件
    UPDATE: 根据传入的file_判断是文件路径还是document object
    """
    if isinstance(file_, str):
        document_object = load_one_file(file_)
    else:
        document_object = file_
    # logger.info("---------开始调用multi-sieve---------\n")
    for sieve in sieve_order:
        pprint(sieve)
        logger.info("Run %s\n" % str(sieve))

        document_object = sieve(document_object)

    # 想好要不要写入文件！
    result_file_path = config.result_folder + document_object.document_file_name + '.v4_result_conll'
    document_object.write_to_file(result_file_path)
    logger.info("-------处理完毕，结果写入 %s-------\n\n"%result_file_path)

    return document_object


def __unit_test(file_):
    document_object = load_one_file(file_)



if __name__ == '__main__':
    import time
    import os
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    test_file = 'small_test2.conll'
    # test_file = 'test.v4_gold_conll'
    test_file_2 = '/opt/tmp/DataSets/conll_test/test/chtb_0249_000.v4_gold_conll'
    res = main(test_file_2)
    print
    key_file = res.original_document_path
    res_file = config.result_folder + res.document_file_name + '.v4_result_conll'

    print key_file
    print res_file
    from Scorer.api_prf import get_one_file_prf
    print get_one_file_prf(key_file, res_file)
    os.remove(res_file)

    # unit_test_utils.print_cluster(res)
    # unit_test_utils.print_gold_cluster(res)

    # __test(test_file)