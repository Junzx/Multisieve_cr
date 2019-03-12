# -*- coding: UTF-8 -*-
import api_one_file
import config
import cPickle
import numpy as np
from pprint import pprint
from os import remove
import ConstantVariable


def get_result(vars = 'train'):
    if vars == 'train':
        folder_path = config.gold_train
    elif vars == 'test':
        folder_path = config.gold_test

    test_files = config.get_var_files(folder_path)
    all_res = {
        'muc': np.array([0.0] * 3),
        'blanc': np.array([0.0] * 3),
        'ceafe': np.array([0.0] * 3),
        'ceafm': np.array([0.0] * 3),
        'bcub': np.array([0.0] * 3),
        'counter': 0
    }
    for file_idx, file_ in enumerate(test_files):
        print file_
        print 'File: %s of %s' % (file_idx, len(test_files))
        print

        prf = api_one_file.main(file_)
        if (prf['muc'] == np.array(['0%', '0%', '0%'])).all() and \
            (prf['ceafm'] == np.array(['0%', '0%', '0%'])).all() and \
            (prf['bcub'] == np.array(['0%', '0%', '0%'])).all():
            # print '可能未找到 跳过'
            # print prf
            continue
        # pprint(prf)

        for key in all_res.keys():
            if key == 'counter':
                all_res['counter'] += 1
                continue
            tmp_ = prf.get(key, [0.0] * 3)
            tmp_ = np.array(map(lambda x: float(x.strip('%')) * 0.01, tmp_))
            all_res[key] += tmp_

        # all_res['muc'] = float(prf['muc'])
        # all_res['blanc'] = float(prf['blanc'])
        # all_res['ceafe'] = float(prf['ceafe'])
        # all_res['ceafm'] = float(prf['ceafm'])
        # all_res['bcub'] = float(prf['bcub'])
        # all_res['counter'] += 1
        print '-' * 30

    with open('all_result.' + api_one_file.sieve_order[-1].__name__, 'wb') as hdl:
        cPickle.dump(all_res, hdl)

def test():
    with open('all_result.' + api_one_file.sieve_order[-1].__name__, 'rb') as hdl:
        all_res = cPickle.load(hdl)

    print '----- 最终结果 -------'
    for key in all_res:
        if key == 'counter':
            continue
        print key, '    ',
        print all_res[key] / all_res['counter']
    print '-' * 30

# --------------------------------------------

def __del_result_files():
    for file_ in config.get_var_files(config.result_folder, 'result'):
        remove(file_)
    print '删除所有result文件！'

def run(vars = 'test'):
    if vars == 'train':
        folder_path = config.gold_train
    elif vars == 'test':
        folder_path = config.gold_test
    elif vars == 'error':
        folder_path = config.error_file_test

    test_files = config.get_var_files(folder_path)[:15]
    for file_idx, file_ in enumerate(test_files):
        # if 'cbs_0029_000' in file_ or \
        #     'dev_09_cmn_0039_000' in file_ or \
        #     'cts_0309_000' in file_:
        #     continue
        print file_
        print 'File: %s of %s' % (file_idx, len(test_files))
        print

        api_one_file.main(file_)

if __name__ == '__main__':
    import time
    start = time.clock()
    print api_one_file.sieve_order[-1].__name__
    # get_result('train')

    # get_result('test')
    # test()
    __del_result_files()

    run('test')
    # run('error')

    print 'use time:', time.clock() - start