# -*- coding: UTF-8 -*-
"""
所有的配置文件
"""
conll_EOF = "\n"
flag_print_sieve_name = False   # 是否打印sieve名字

from os import listdir, name, getcwd
from getpass import getuser

def get_var_files(folder_path, var = 'gold'):
    return [folder_path  + f_ for f_ in listdir(folder_path) if var in f_]

# ====================================================

if name == 'posix':
    separator = '/'

    if getuser() == 'zz':   # sony linux
        basic_folder = '/opt/tmp/DataSets/conll_test/'

    elif getuser() == 'yqzhu':  # server linux
        basic_folder = '/home/yqzhu/conll_test/'

    path_log_folder = basic_folder + 'log'
    gold_train = basic_folder + 'train/data_go/'
    gold_test = basic_folder + 'test/'

# ----------------------------

elif name == 'nt':
    pass

# ====================================================

def __unit_test():
    from pprint import pprint
    pprint(basic_folder)
    pprint(path_log_folder)
    pprint(gold_test)
    pprint(gold_train)

if __name__ == '__main__':
    __unit_test()