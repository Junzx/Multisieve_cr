# -*- coding: UTF-8 -*-
"""
所有的配置文件
"""
conll_EOF = "\n"
flag_print_sieve_name = False   # 是否打印sieve名字

from os import listdir, name, getcwd
from getpass import getuser

if name == 'posix':
    if getuser() == 'zz':   # sony linux
        separator = '/'
        basic_folder = "/media/zz/3188e54f-274b-49fa-ac08-3585cf577a28/zz/conll_test/"
        path_log_folder = basic_folder + 'log'
        gold_train = 'train/data_go/'
        gold_test = 'test/'

elif name == 'nt':
    pass