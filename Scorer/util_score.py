# coding=utf-8
import config
import FilePath
from os import popen,getcwd,name,remove,listdir
from shutil import copy
from time import clock

# path_folder = FilePath.path_small_test_floder
# path_folder = FilePath.path_test_folder
path_folder = FilePath.path_test_pronoun_folder
separator = '/'

def run_scorer():
    print 'Run scorer'
    start = clock()
    # util_conll.delete_files(config.prf_result)
    #
    # if name == 'posix':   # 服务器路径
    #     config_file = '/home/yqzhu/Subject/config.py'
    # elif getuser() == 'zx': # Lab
    #     config_file = 'D:\MyGitHub\Subject\config.py'
    # elif getuser() == 'zyq19':  # laptop
    #     config_file = 'I:\GitHub\Subject\config.py'
    #
    # copy(config_file,getcwd())
    # import config
    # def load_data(data_type):
    #     folder = config.file_folder
    #     return [folder + i for i in listdir(folder) if i.endswith('v4_' + data_type + '_conll')]
    # lst_gold = load_data(config.data_type)
    # lst_gold_result = load_data(config.sieve_result)
    # lst_gold_result = load_data('test_result')  # 处理gold生成的数据
    gold_data_folder = path_folder  # 原始目录 gold和result文件所在的目录
    data = listdir(gold_data_folder)  # 该目录下所有文件
    gold_data = [path for path in data if 'gold' in path]
    result_data = [path for path in data if 'result' in path]
    lst_tmp_gold = [i.split('.')[0] for i in gold_data]
    lst_tmp_gold_result = [i.split('.')[0] for i in result_data]
    set_score_conll = set(lst_tmp_gold).intersection(set(lst_tmp_gold_result))
    counter = 0
    for file_name in list(set_score_conll):

        # 待处理的文件名
        gold_file = file_name + '.v4_gold_conll'
        result_file = file_name + '.v4_result_conll'

        # 待复制的两个文件的路径
        str_path_gold = gold_data_folder + separator + gold_file
        str_path_gold_result = gold_data_folder + separator + result_file

        # 从源路径拷贝过来
        copy(str_path_gold, getcwd())
        copy(str_path_gold_result, getcwd())

        # 拼凑调用的命令
        muc_order = 'perl scorer.pl muc ' + gold_file + ' ' + result_file
        bcub_order = 'perl scorer.pl bcub ' + gold_file + ' ' + result_file
        ceafe_order = 'perl scorer.pl ceafe ' + gold_file + ' ' + result_file
        blanc_order = 'perl scorer.pl blanc ' + gold_file + ' ' + result_file

        # prf log 文件名
        prf_file = file_name + '_prf.txt'
        # str_path_prf = file_name.split('\\')[-1] + '.v4_' + config.prf_result + '_conll'
        counter += 1
        print counter,prf_file

        # 调用评价的perl程序
        with open(prf_file, 'a') as hdl_prf:
            muc_output = popen(muc_order)
            bcub_output = popen(bcub_order)
            ceafe_output = popen(ceafe_order)
            blanc_output = popen(blanc_order)

            hdl_prf.write('\n' + '-' * 30 + 'muc' + '-' * 30 + '\n')
            for line in muc_output.read():
                hdl_prf.write(line)

            hdl_prf.write('\n' + '-' * 30 + 'bcub' + '-' * 30 + '\n')
            for line in bcub_output.read():
                hdl_prf.write(line)

            hdl_prf.write('\n' + '-' * 30 + 'ceafe' + '-' * 30 + '\n')
            for line in ceafe_output.read():
                hdl_prf.write(line)

            hdl_prf.write('\n' + '-' * 30 + 'blanc' + '-' * 30 + '\n')
            for line in blanc_output.read():
                hdl_prf.write(line)

        # 将prf文件复制回文件夹
        # from_folder = '\\'.join(file_name.split('\\')[:-1]) # 源文件夹的名字，用于复制回去
        copy(prf_file, gold_data_folder)

        # 删除prf文件和conll文件
        remove(prf_file)
        remove(gold_file)
        remove(result_file)
    print "用了:", clock() - start, 's'
    print "生成了：", counter, '个prf结果文件'

if __name__ == '__main__':
    run_scorer()

