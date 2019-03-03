# coding: utf-8
"""
统计conll文件的信息，包括document个数、token个数、表述个数、实体个数
"""
import os
from SubjectUtils import unit_test_utils
import config
import LoadConll

def get_var_files(folder, var='bn'):
    return [folder + i for i in os.listdir(folder) if i.startswith(var)]

def get_result(var='bn'):
    # train
    # _files = get_var_files(config.gold_train, var)

    # test
    _files = config.get_var_files(config.gold_test, 'gold')
    result_file_nums = len(_files)  # 文件个数

    counter_token = 0
    counter_mention = 0
    counter_entity = 0

    for file_ in _files:
        data = LoadConll.load_one_file(file_)

        counter_token += len(data.lst_tokens)
        counter_mention += len(data.lst_mentions)
        counter_entity += len(unit_test_utils.get_entities(data).keys())
    return result_file_nums, counter_token, counter_mention, counter_entity



if __name__ == '__main__':
    # 统计train文件
    # vars = ['bn', 'mz', 'nw', 'bc', 'wb', 'tc']
    # for var in vars:
    #     print var
    #     print get_result(var)

    # 统计test文件
    print get_result()