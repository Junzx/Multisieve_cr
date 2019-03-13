# coding: utf-8

import api_one_file
import api_md_one_file
import config
import LoadConll
from os import remove

files = config.get_var_files(config.gold_test)#[:10]

def __del_result_files():
    for file_ in config.get_var_files(config.result_folder, 'result'):
        remove(file_)
    print '删除所有result文件！'

def main(file_):
    # print '=============='
    md_res_obj = api_md_one_file.main(file_)
    # for m in md_res_obj.lst_mentions:
    #     print m.chinese_word, m.mention_id, m
    # print '-------------------'
    res = api_one_file.main(md_res_obj)

    # gold_obj = LoadConll.load_one_file(file_)
    # gold_res = api_one_file.main(gold_obj)
    return res

if __name__ == '__main__':
    __del_result_files()

    for file_idx, file_ in enumerate(files):
        # if 'cbs_0029_000' in file_ or \
        #     'dev_09_cmn_0039_000' in file_ or \
        #     'cts_0309_000' in file_:
        #     continue
        # if 'cmn_0059' not in file_:
        #     continue
        print file_
        print 'File: %s of %s' % (file_idx, len(files))
        print

        main(file_)

