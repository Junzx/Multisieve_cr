# -*- coding: UTF-8 -*-
import api_one_file
import config
import cPickle
import numpy as np
from pprint import pprint


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
        pprint(prf)

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

    for key in all_res:
        if key == 'counter':
            continue
        print key, '    ',
        print all_res[key] / all_res['counter']
    print '-' * 30

if __name__ == '__main__':
    import time
    start = time.clock()
    print api_one_file.sieve_order[-1].__name__
    # get_result('train')

    get_result('test')
    test()

    print 'use time:', time.clock() - start