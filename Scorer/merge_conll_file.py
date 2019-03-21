# -*- coding: UTF-8 -*-
"""
给定两个文件夹，合并文件
"""
import config
import os

def __merge_file(folder_path, function_file_path, var = 'gold'):
    """
    注：顺序应该无所谓
    :param folder_path: 待合并文件的文件夹路径
    :param function_file_path: 生成文件的文件路径
    :param var: 包含的关键字，如gold，result等
    """
    files = [folder_path + f_ for f_ in os.listdir(folder_path) if var in f_]
    with open(function_file_path, 'w') as hdl:
        for one_file in files:
            # print 'write file: %s'%one_file
            with open(one_file, 'r') as one_file_hdl:
                hdl.write(one_file_hdl.read())
                hdl.write('\n\n')


def api_(var='gold'):
    if var == 'result':
        folder_path = config.result_folder
        function_file_path = config.project_path + '/Scorer/merged_test.v4_result_conll'
        __merge_file(folder_path, function_file_path, 'result')
    elif var == 'test':
        folder_path = config.gold_test
        function_file_path = config.project_path + '/Scorer/merged_test.v4_gold_conll'
        __merge_file(folder_path, function_file_path, 'gold')
    elif var == 'train':
        folder_path = config.gold_train
        function_file_path = config.project_path + '/Scorer/merged_test.v4_gold_conll'
        __merge_file(folder_path, function_file_path, 'gold')




if __name__ == '__main__':
    var = 'result'
    api_(var)
