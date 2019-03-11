# coding: utf-8

import api_one_file
import api_md_one_file
import config
from os import remove

files = config.get_var_files(config.gold_test)

def __del_result_files():
    for file_ in config.get_var_files(config.result_folder, 'result'):
        remove(file_)
    print '删除所有result文件！'

def main(file_):
    md_res_obj = api_md_one_file.main(file_)
    res = api_one_file.main(md_res_obj)
    return res

if __name__ == '__main__':
    __del_result_files()

    for file_idx, file_ in enumerate(files):
        # if 'cbs_0029_000' in file_ or \
        #     'dev_09_cmn_0039_000' in file_ or \
        #     'cts_0309_000' in file_:
        #     continue
        print file_
        print 'File: %s of %s' % (file_idx, len(files))
        print

        main(file_)

