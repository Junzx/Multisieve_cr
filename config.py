# -*- coding: UTF-8 -*-
"""
所有的配置文件
"""
import os
conll_EOF = "\n"
flag_print_sieve_name = False   # 是否打印sieve名字

from os import listdir, name, getcwd
from getpass import getuser


# ========================================
# =============== 开 关 ===================
# ========================================
flag_load_corenlp = True   # 注意！！！如果flag为True，会导致不打印log
flag_jump_corefed_mention = False   # 是否跳过已经指代的表述



# ========================================
# ============= 基本属性 ==================
# ========================================
def get_var_files(folder_path, var = 'gold'):
    return [folder_path + f_ for f_ in listdir(folder_path) if var in f_]

project_path = os.path.dirname(__file__)


if name == 'posix':
    separator = '/'

    if getuser() == 'zz':   # sony linux
        basic_folder = '/opt/tmp/DataSets/conll_test/'
        # nlp_path = '/opt/tmp/stanford-corenlp-full-2018-10-05'
        embedding_dim = 50
        embedding_path = '/opt/tmp/DataSets/zuowen.vectors.50'

    elif getuser() == 'yqzhu':  # server linux
        basic_folder = '/home/yqzhu/conll_test/'
        nlp_path = '/home/yqzhu/stanford-corenlp-full-2018-10-05'

    path_log_folder = basic_folder + 'log'
    gold_train = basic_folder + 'train/data_go/'
    gold_dev = basic_folder + 'development/data_go/'
    gold_test = basic_folder + 'test/'
    result_folder = basic_folder+ 'result/'
    error_file_test = basic_folder + 'Error_/'

# ----------------------------

elif name == 'nt':
    if getuser() == 'T480':
        nlp_path = 'D:\stanford-corenlp-full-2018-10-05\\'

    separator = '\\'
    basic_folder = r'E:\conll_test\\'
    path_log_folder = basic_folder + 'log\\'
    gold_train = basic_folder + 'train\data_go\\'
    gold_dev = basic_folder + 'development\data_go\\'
    gold_test = basic_folder + 'test\\'
    result_folder = basic_folder+ 'result\\'
    error_file_test = basic_folder + 'Error_\\'


# ====================================================

def __unit_test():
    from pprint import pprint
    pprint(basic_folder)
    pprint(path_log_folder)
    pprint(gold_test)
    pprint(gold_train)
    pprint(project_path)

if __name__ == '__main__':
    __unit_test()