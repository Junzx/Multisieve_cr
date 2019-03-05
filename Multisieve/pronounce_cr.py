# -*- coding: UTF-8 -*-
"""
这个文件主要处理第三人称代词
"""
# -*- coding: UTF-8 -*-
import config
import os
import ConstantVariable
from SubjectUtils.sieve_utils import get_candidate_mentions
from pprint import pprint
from math import fabs


def pronoun_sieve(obj_document):
    if config.flag_print_sieve_name:
        print('pronoun sieve')

    # - func 找到代词表述
    pronoun_mentions = []
    for mention in obj_document.lst_mentions:
        if mention.chinese_word in ConstantVariable.pronouns:
            pronoun_mentions.append(mention)


    # - func 针对代词选取候选先行语，约束句子举例小于等于3
    for p_m in pronoun_mentions:
        # candidate_mentions = [mention for mention in obj_document.lst_mentions[:p_m.mention_id]\
        #                       if fabs(mention.sent_id - p_m.sent_id) <= 3]
        candidate_mentions = get_candidate_mentions(obj_document, p_m)

        # - func 从候选表述中依次进行判断
        for candidate_m in candidate_mentions:

            # - rule 如果动物属性相同（只有相同的适合相乘才可能等于1）
            # if candidate_m.animacy * p_m.animacy == 1:


            # 实验1： 使用所有属性
            # if candidate_m.gender == p_m.gender and \
            #     candidate_m.animacy == p_m.animacy and \
            #     candidate_m.single == p_m.single:
            #     obj_document.set_coref(candidate_m, p_m)
            #     break


            # 实验2： 仅使用动物属性
            if candidate_m.animacy == p_m.animacy and \
                fabs(candidate_m.sent_id - p_m.sent_id) <= 3:
                obj_document.set_coref(candidate_m, p_m)
                break

    return obj_document


if __name__ == '__main__':
    import load_conll

    orig_path = os.path.abspath('..')
    data = load_conll.load_one_file(orig_path + '\\test.v4_gold_conll')
    data.print_gold_cluster()
    # pronoun_sieve(data)