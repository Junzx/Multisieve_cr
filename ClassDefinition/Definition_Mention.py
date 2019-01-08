# -*- coding: UTF-8 -*-
from __future__ import division
import UserCorpus.api_user_corpus as user_corpus
from copy import deepcopy
import ConstantVariable
import UserCorpus

class Mention(object):
    def __init__(self):
        # 以下属性在创建对象的时候就要传入
        self.mention_id = 0 # 每个mention的唯一uid
        self.entity_id = 0  # mention对应的实体id
        self.gold_entity_id = 0 # mention的标准的答案
        self.lst_tokens = [] # 在创建这个对象的时候就要传入参数

        # 以下属性在创建时仅定义，赋值留给下面的set_other_attributes()函数操作
        self.sent_id = 0    # 该mention所在的句子 的id
        self.start_token_id = 0 # 这个mention 开始的token id
        self.end_token_id = 0   # 这个mention 最后的token id
        self.chinese_word = ''  # 中文
        self.head_word = ''     # 中心词
        self.ner = '-'          # 命名实体标签
        self.pos_info = '-'     # pos标记
        self.parse = '-'        # parse信息

        self.weight = 0.0  # 当前这个mention的权重，默认为0

        # 增加一系列属性,是entity级别的信息
        self.entity_attr_gender = 0
        self.entity_attr_number = 0
        self.entity_attr_animacy = 0

    def set_other_attributes(self, lst_tokens):
        """
        用来设置其他的属性
        """
        self.start_token_id = lst_tokens[0].token_id
        self.end_token_id = lst_tokens[-1].token_id
        self.sent_id = lst_tokens[0].sent_id
        self.chinese_word = self.__set_chinese_word(lst_tokens)
        self.head_word = self.__set_head_word(lst_tokens) # 中心词
        self.ner = self.__set_ner(lst_tokens) # 命名实体标签
        self.pos_info = self.__set_pos(lst_tokens)    # pos
        self.parse = self.__set_parse(lst_tokens)     # parse
        self.animacy = self.__set_animacy()         # unknown-0/Animal-1/Inanimate--1
        self.gender = self.__set_gender()           # unknown-0/Male-1/Female--1
        self.single = self.__set_single()           # unknown-0/Single-1/Plural--1


    def __set_chinese_word(self,lst_tokens):
        """
        根据lst_token拼接mention对应的中文文本
        """
        return ''.join([token.word_itself for token in lst_tokens])

    def __set_head_word(self, lst_tokens):
        """
        得到中心词，这种方法不准确，需要再处理
        """
        # 说明NP的head word是本身
        if len(lst_tokens) == 1:
            return self.chinese_word

        # 取最后一个token的中文作为head word
        elif len(lst_tokens) > 1:
            return lst_tokens[-1].word_itself

    def __set_ner(self,lst_tokens):
        return lst_tokens[-1].ner

    def __set_pos(self, lst_tokens):
        if len(lst_tokens) == 1:   # 如果只有一个token
            return lst_tokens[0].pos_info
        else:
            return lst_tokens[-1].pos_info     # 返回head word的pos

    def __set_parse(self, lst_tokens):
        if len(lst_tokens) == 1:
            return lst_tokens[0].parse_info
        else:
            return ''.join([token.parse_info for token in lst_tokens])

    def __set_gender(self):
        if u'他' in self.chinese_word:
            return 1
        elif u'她' in self.chinese_word:
            return -1
        elif self.chinese_word in user_corpus.get_pca_list():
            return -1
        return 0

    def __set_animacy(self):
        if self.ner == 'PERSON' or self.pos_info == 'PN':
            return 1
        elif self.chinese_word in ConstantVariable.pronouns:
            return 1
        elif self.ner in ConstantVariable.ner_labels:
            return -1
        elif self.chinese_word in user_corpus.get_nation():
            return -1
        elif self.chinese_word in ['它','它们']:
            return -1
        elif self.chinese_word in user_corpus.get_pca_list():
            return -1
        return 0

    def __set_single(self):
        # 设置single
        if self.ner in ('ORGANIZATION', 'GPE'):
            return -1
        elif self.ner == 'PERSON':
            return 1
        for char in list(u'多一二三四五六七八九十百千万'):
            if char in self.chinese_word:
                return -1
        if '们' in self.chinese_word:
            return -1
        elif self.chinese_word in user_corpus.get_pca_list():
            return 1
        # if self.chinese_word in ConstantVariable.pronouns:
        #     return 1
        # if self.chinese_word in UserCorpus.get_adj_nation():
        #     return 1
        return 0

    def get_modifier(self):
        """
        获取当前表述的修饰语
        的：DEC\DEG
        地：DEV
        得：DER
        """
        flag_modifier = False
        index_determiner_token = 0
        for index_token,token in enumerate(self.lst_tokens):
            # print token.word_itself,'/',
            if token.pos_info in ['DEC','DEG','DEV']:
            # if token.word_itself == '的':
                flag_modifier = True
                index_determiner_token = index_token
        if flag_modifier:
            modifier = ''
            for token in self.lst_tokens[:index_determiner_token]:
                modifier += token.word_itself
            return modifier
        else:
            return 'No-modifier'

    def get_determiner(self):
        """
        获取当前表述的限定词，token的pos tag为：DT/CD/OD
        """
        for token in self.lst_tokens:
            if token.pos_info in ['DT','CD','OD']:
                return token.word_itself
        return 'No-determiner'

    def get_class_attribute(self):
        return self.__dict__
