# -*- coding: UTF-8 -*-
"""
给定两个文件夹，合并文件
"""
import config
import os

def merge_file(folder_path, function_file_path, var = 'gold'):
    """
    注：顺序应该无所谓
    :param folder_path: 待合并文件的文件夹路径
    :param function_file_path: 生成文件的文件路径
    :param var: 包含的关键字，如gold，result等
    :return:
    """
    files = [folder_path + f_ for f_ in os.listdir(folder_path) if var in f_]
    with open(function_file_path, 'w') as hdl:
        for one_file in files:
            print 'write file: %s'%one_file
            with open(one_file, 'r') as one_file_hdl:
                hdl.write(one_file_hdl.read())
                hdl.write('\n\n')

    print 'finish!'


if __name__ == '__main__':
    # result_path = config.result_folder
    # var = 'result'

    gold_path = config.gold_test
    var = 'gold'

    function_file_path = 'merged_test.v4_%s_conll'%var

    merge_file(gold_path, function_file_path, var)