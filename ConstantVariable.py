# -*- coding: UTF-8 -*-
"""
一些定义的常量
"""
from copy import deepcopy


first_person_pronouns = [u'我',u'我们',u'咱',u'咱们',u'本人']
second_person_pronouns = [u'你',u'你们',u'您',u'您们',u'尔',u'尔等']
third_person_pronouns = [u'他',u'她',u'它',u'他们',u'她们',u'它们']

# 表达是人的代词
human_pronounces = [u'他',u'她',u'他们',u'她们']
human_pronounces.extend(first_person_pronouns)
human_pronounces.extend(second_person_pronouns)

pronouns = deepcopy(first_person_pronouns)
pronouns.extend(second_person_pronouns)
pronouns.extend(third_person_pronouns)


# 固定返回的字符串
CONST_STRING_NO_MODIFIER = 'No-modifier'
CONST_STRING_NO_DETERMINER = 'No-determiner'

comma = (u',', u'，')                            # 中英文逗号
word_bag_is = (u'是', u'即', u'就是', u'也就是')   # 表示is的词语
speak_verbs_set = (u'说',u'表示',u'认为')         # 表示 说的词语


# 所有遇到的NER标签
ner_labels = ['*', 'ORDINAL', 'LOC', 'PRODUCT', 'NORP',
             'WORK_OF_ART', 'LANGUAGE', 'PERCENT', 'GPE',
             'MONEY', 'TIME', 'CARDINAL', 'FAC', 'DATE',
             'ORG', 'LAW', 'EVENT', 'QUANTITY']