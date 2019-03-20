# -*- coding: UTF-8 -*-
"""
一些定义的常量
"""
from copy import deepcopy
from time import clock
import config

first_person_pronouns = [u'我',u'我们',u'咱',u'咱们',u'本人']
second_person_pronouns = [u'你',u'你们',u'您',u'您们',u'尔',u'尔等']
third_person_pronouns = [u'他',u'她',u'它',u'他们',u'她们',u'它们']

# 表达是人的代词
human_pronounces = [u'他',u'她',u'他们',u'她们']
human_pronounces.extend(first_person_pronouns)
human_pronounces.extend(second_person_pronouns)
# 表达非人的代词
no_human_pronounces = [u'它', u'它们']

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
ner_labels = ['ORDINAL', 'LOC', 'PRODUCT', 'NORP',
             'WORK_OF_ART', 'LANGUAGE', 'PERCENT', 'GPE',
             'MONEY', 'TIME', 'CARDINAL', 'FAC', 'DATE',
             'ORG', 'LAW', 'EVENT', 'QUANTITY']

# 读取cnn结果
from Experiment.ExperimentResult.load_mention_info_result import get_animacy_info_dict, get_gender_info_dict
__animacy_dict = get_animacy_info_dict()
__gender_dict = get_gender_info_dict()

def get_animacy(str_):
    tmp_ = __animacy_dict.get(str_, None)
    if tmp_ == 0.0:
        return 1
    elif tmp_ == 1.0:
        return -1
    else:
        return 0

def get_gender(str_):
    tmp_ = __gender_dict.get(str_, None)
    if tmp_ == 0.0:
        return 1
    elif tmp_ == 1.0:
        return -1
    else:
        return 0

# 加载字典
from UserCorpus import load_corpus
start = clock()
corpus_dict = {
    'quantifier': load_corpus.get_quantifier(),
    'nation': load_corpus.get_nation(),
    'adj_nation': load_corpus.get_adj_nation(),
    'stop_word': load_corpus.get_stop_words(),
    'report_verb': load_corpus.get_report_verbs(),
    'determiner_word': load_corpus.get_determiner_words(),
    'conjunction_word': load_corpus.get_conjunction_words(),
    'verb': load_corpus.get_verbs(),
    'animal': load_corpus.get_animals(),
    'botanical': load_corpus.get_botanical(),
    'synonym_word': load_corpus.get_synonym_words(),
    'pca_list': load_corpus.get_pca_list(),
    'abbreviation_dict': load_corpus.get_abbreviation_dict(),
}
# print 'load corpus: ', clock() - start

if config.flag_load_corenlp:
    from stanfordcorenlp import StanfordCoreNLP
    nlp_handle = StanfordCoreNLP(config.nlp_path, lang='zh')