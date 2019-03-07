# -*- coding: UTF-8 -*-
import api_md_one_file
import config

def run(vars = 'test'):
    if vars == 'train':
        folder_path = config.gold_train
    elif vars == 'test':
        folder_path = config.gold_test
    elif vars == 'error':
        folder_path = config.error_file_test

    test_files = config.get_var_files(folder_path)
    all_p = all_r = all_f = all_counter = 0.0
    for file_idx, file_ in enumerate(test_files):
        # if 'cnr_0019_000.v4_gold_conll' not in file_:
        #     continue
        print file_
        print 'File: %s of %s' % (file_idx, len(test_files))
        res = api_md_one_file.main(file_)
        print res
        all_counter += 1
        all_p += res[0]
        all_r += res[1]
        all_f += res[2]

    print '---------------', all_counter, '-------------'
    print all_p / all_counter
    print all_r / all_counter
    print all_f / all_counter
    print

if __name__ == '__main__':
    import time

    start = time.clock()

    run('test')

    print 'use time:', time.clock() - start