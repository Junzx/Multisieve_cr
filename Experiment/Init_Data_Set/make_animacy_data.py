# -*- coding: UTF-8 -*-
"""
读取train/test目录下所有文件，抽取其中的动物属性词语和非动物属性词语
"""
import config
import LoadConll
import ConstantVariable
import random
from SubjectUtils.unit_test_utils import print_gold_cluster

# nums = 1078 # test条数
nums = 6840 # train条数

# ---------------------------------------


def get_animacy_mention(file_):
    """
    ！构建Animacy词语
    获取一个conll文件路径，load进来
    抽取其中指代指人的表述
    """
    data = LoadConll.load_one_file(file_)
    human_word_list = []

    # 构建实体cluster
    entity_dic = {}
    for mention in data.gold_mention:
        if mention.gold_entity_id not in entity_dic:
            entity_dic.setdefault(mention.gold_entity_id, [])
        entity_dic[mention.gold_entity_id].append(mention)

    # 对dict处理
    for entity_id, entity_cluster in entity_dic.items():
        for mention in entity_cluster:
            # 如果有代词
            if mention.chinese_word in ConstantVariable.human_pronounces:
                human_word_list.extend([m.chinese_word for m in entity_cluster])
                break

            # 如果NER为PERSON
            if mention.ner == 'PERSON':
                human_word_list.extend([m.chinese_word for m in entity_cluster])
                break

    return human_word_list

def make_human_data_set():
    var = 'train'
    function_folder = config.gold_train

    # var = 'test'
    # function_folder = config.gold_test

    human_word_list = []
    for file_ in config.get_var_files(function_folder):
        tmp_ = get_animacy_mention(file_)
        human_word_list.extend(tmp_)

    with open(var + '_human.txt', 'w') as hdl:
        for word in set(human_word_list):
            hdl.write(word + '\n')

# ---------------------------------------

def get_inanimacy_mention(file_):
    """
    ！构建非 Animacy词语
    获取一个conll文件路径，load进来
    抽取其中指代指人的表述
    """
    data = LoadConll.load_one_file(file_)
    no_human_word_list = []

    # 构建实体cluster
    entity_dic = {}
    for mention in data.gold_mention:
        if mention.gold_entity_id not in entity_dic:
            entity_dic.setdefault(mention.gold_entity_id, [])
        entity_dic[mention.gold_entity_id].append(mention)

    # 对dict处理
    for entity_id, entity_cluster in entity_dic.items():
        for mention in entity_cluster:
            # 如果有代词
            if mention.chinese_word in ConstantVariable.no_human_pronounces:
                no_human_word_list.extend([m.chinese_word for m in entity_cluster])
                break

            # 如果NER为PERSON
            if mention.ner != 'PERSON' and mention.ner != '*':
                no_human_word_list.extend([m.chinese_word for m in entity_cluster])
                break

        if len(no_human_word_list) >= nums * 5:
            print '数量够了'
            break

    return no_human_word_list


def make_no_human_data_set():

    var = 'train'
    function_folder = config.gold_train

    # var = 'test'
    # function_folder = config.gold_test

    no_human_word_list = []
    for file_ in config.get_var_files(function_folder):
        tmp_ = get_inanimacy_mention(file_)
        no_human_word_list.extend(tmp_)

    with open(var + '_non_human.txt', 'w') as hdl:
        # if len(no_human_word_list) <= nums:
        #     choice_sample = list(set(no_human_word_list))
        # else:
        #     choice_sample = random.sample(list(set(no_human_word_list)), nums - 1)
        choice_sample = set(no_human_word_list)
        for word in choice_sample:
            hdl.write(word + '\n')

def __unit_test():

    file_ = '/opt/tmp/GithubCodes/Multisieve_cr/test.v4_gold_conll'
    for i in get_animacy_mention(file_):
        print i


if __name__ == '__main__':
    # __unit_test()

    # make_human_data_set()
    make_no_human_data_set()