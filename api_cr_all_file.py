# -*- coding: UTF-8 -*-
import api_cr_one_file
import config
import cPickle
import numpy as np
from pprint import pprint
from os import remove
import ConstantVariable

import logging
# logging.basicConfig(filename=config.project_path + "/RunResults/MyLog.log",
#                     level=logging.INFO, filemode='a')
logger = logging.getLogger("Coreference_Experiment_All")


def __del_result_files():
    """
    删除 config.result路径下文件
    :return:
    """
    counter = 0
    for file_ in config.get_var_files(config.result_folder, 'result'):
        counter += 1
        remove(file_)
    pprint(u'Deleted %s result Files！'%counter)

def run(vars = 'test'):
    if vars == 'train':
        folder_path = config.gold_train
    elif vars == 'test':
        folder_path = config.gold_test
    elif vars == 'error':
        folder_path = config.error_file_test

    test_files = config.get_var_files(folder_path)#[:10]
    for file_idx, file_ in enumerate(test_files):
        pprint('----------------%s-------------' % file_)
        pprint('File: %s of %s' % (file_idx, len(test_files)))
        api_cr_one_file.main(file_)


if __name__ == '__main__':
    import time
    start = time.clock()

    __del_result_files()
    logger.info('From api_cr_all_files.py')

    run('test')

    pprint('use time: %s'% (time.clock() - start))