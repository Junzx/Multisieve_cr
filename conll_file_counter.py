# coding: utf-8
import os
from SubjectUtils import unit_test_utils
import config
import LoadConll

def get_var_files(folder, var='bn'):
    return [folder + i for i in os.listdir(folder) if i.startswith(var)]

def get_result(var='bn'):
    _files = get_var_files(config.gold_train, var)
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
    print get_result('bn')