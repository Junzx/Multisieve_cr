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


def get_male_mention(file_):
    """
    男人
    """
    data = LoadConll.load_one_file(file_)
    male_word_list = []

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
            if mention.chinese_word in [u'他', u'他们']:
                male_word_list.extend([m.chinese_word for m in entity_cluster])
                break

            # 如果NER为PERSON
            # if mention.ner == 'PERSON':
            #     human_word_list.extend([m.chinese_word for m in entity_cluster])
            #     break

    return male_word_list

def make_male_data_set(vars):
    if vars == 'train':
        var = 'train'
        function_folder = config.gold_train
    elif vars == 'test':
        var = 'test'
        function_folder = config.gold_test

    # var = 'test'
    # function_folder = config.gold_test

    human_word_list = []
    for file_ in config.get_var_files(function_folder):
        tmp_ = get_male_mention(file_)
        human_word_list.extend(tmp_)

    with open(var + '_male.txt', 'w') as hdl:
        for word in set(human_word_list):
            hdl.write(word + '\n')

# ---------------------------------------

def get_female_mention(file_):
    """

    """
    data = LoadConll.load_one_file(file_)
    female_word_list = []

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
            if mention.chinese_word in [u'她', u'她们']:
                female_word_list.extend([m.chinese_word for m in entity_cluster])
                break

        if len(female_word_list) >= nums * 5:
            print '数量够了'
            break

    return female_word_list


def make_female_data_set(vars='test'):
    if vars == 'train':
        var = 'train'
        function_folder = config.gold_train
    elif vars == 'test':
        var = 'test'
        function_folder = config.gold_test

    no_human_word_list = []
    for file_ in config.get_var_files(function_folder):
        tmp_ = get_female_mention(file_)
        no_human_word_list.extend(tmp_)

    with open(var + '_female.txt', 'w') as hdl:
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
    make_female_data_set('train')
    print '1'
    make_male_data_set('train')
    print '2'
    make_male_data_set('test')