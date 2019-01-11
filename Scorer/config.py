# -*- coding: UTF-8 –*-
__author__ = 'candnes'
from os import listdir
from os import name,getcwd
from getpass import getuser



# 使用dev还是train数据
data_folder = r'development'
# data_folder = r'train'

# data_ = 'data_au'
data_ = 'data_go'

data_type = 'gold'
md_result = 'my_' + data_type
sieve_result = md_result + '_result'
prf_result = md_result + '_prf'

# order = [0,11]
order = range(10) + [11]

# 数据的路径
if name == 'posix':   # 服务器路径
    file_folder = '/home/yqzhu/conll_test/' + data_folder + '/' + data_ + '/'
    log_document_name = '/home/yqzhu/Log_All_Files/'
    score_pl = 'home/yqzhu/Subject/Scorer/util_score.py'
    config = 'home/yqzhu/Subject/config.py'
    EOF = '\r\n'

elif getuser() == 'zx': # Lab
    file_folder = 'D:\conll test\\' + data_folder + '\\' + data_ + '\\'
    log_document_name = 'D:\MyGitHub\Log_All_Files\\'
    score_pl = 'D:\MyGitHub\Subject\Scorer\util_score.py'
    config = 'D:\MyGitHub\Subject\config.py'
    # file_folder = 'D:\MyGitHub\\test\\'
    # log_document_name = 'D:\MyGitHub\\test\\'
    # file_folder = 'D:\conll test\my_test\\'

    EOF = '\n'

elif getuser() == 'zyq19':  # laptop
    file_folder = 'I:\conll test\\' + data_folder + '\\' + data_ + '\\'
    score_pl = 'I:\GitHub\Subject\Scorer\util_score.py'
    log_document_name = 'I:\Log_All_Files\\'
    config = 'I:\GitHub\Subject\config.py'
    EOF = '\n'

if __name__ == '__main__':
    print repr(EOF)
    # print auto_conll
    # with open(auto_conll, 'r') as hdl:
    #     for i in hdl.readlines()[:10]:
    #         print i.strip('\n')