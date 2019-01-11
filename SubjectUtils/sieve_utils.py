# -*- coding: UTF-8 -*-
"""
放cr过程中需要的函数

- get_candidate_mentions()  # 获取候选表述
- get_modifier()            # 获取mention的修饰语
"""
from math import fabs
import ConstantVariable

def word_similiar(word1, word2):
    return 0.8

def get_candidate_mentions(obj_document, obj_mention):
    """
    给定mention并返回候选表述
    目前实现：
        设定句子距离为2，返回前几个句子的表述作为候选
    TODO：
        1. 获取mention的句子id
        2. 获取前n=3个sent对象（包括当前表述所在的句子）
        3. 从后向前选择sent对象，其中表述按照从左向右选取
    """
    sentence_distance = 1  # 表示 表述所在的句子，以及之前的 n 个句子
    if obj_mention.mention_id == 0:
        return []
    candidate_mentions = []
    sent_id = obj_mention.sent_id
    mention_id = obj_mention.mention_id
    for candidate_m in obj_document.lst_mentions:
        if str(candidate_m.entity_id).startswith('E_'):
            continue
        if candidate_m.sent_id <= sent_id and \
                fabs(candidate_m.sent_id - sent_id) <= sentence_distance and \
                candidate_m.mention_id != mention_id:
            candidate_mentions.append(candidate_m)

        elif candidate_m.mention_id == mention_id or candidate_m.sent_id > sent_id:
            break
    return candidate_mentions

def get_modifier_old(mention):
    """
    获取当前表述的修饰语
    的：DEC\DEG
    地：DEV
    得：DER
    :param mention: 输入一个mention对象
    :return:
        - 如果有修饰语，则返回修饰语文本
        - 如果没有，返回固定字符串
    """
    flag_modifier = False
    index_determiner_token = 0
    for index_token,token in enumerate(mention.lst_tokens):
        if token.pos_info in ['DEC','DEG','DEV']:
            flag_modifier = True
            index_determiner_token = index_token

    if flag_modifier:
        modifier = ''
        for token in mention.lst_tokens[:index_determiner_token]:
            modifier += token.word_itself
        return modifier
    else:
        return ConstantVariable.CONST_STRING_NO_MODIFIER

def get_determiner(mention):
    """
    获取当前表述的限定词，token的pos tag为：DT/CD/OD
        :param mention: 输入一个mention对象
    :return:
        - 如果有限定词，则返回限定词文本
        - 如果没有，返回固定字符串
    """
    for token in mention.lst_tokens:
        if token.pos_info in ['DT','CD','OD']:
            return token.word_itself
    return ConstantVariable.CONST_STRING_NO_DETERMINER

def get_modifier(obj_sentence, mention):
    """
    获取修饰语
    """
    # 1. 先检查mention中是否有 ‘的地得’
    for token_idx, token in enumerate(mention.lst_tokens):
        if token.pos_info in ['DEC', 'DEG', 'DEV']:    # 是 的地得
            return ''.join([t.word_itself for t in mention.lst_tokens[:token_idx]])

    # 2. 如果没有，那么检查包含这个表述的这个句子
    if mention not in obj_sentence.lst_mentions:
        return ConstantVariable.CONST_STRING_NO_MODIFIER

    # DEC_token_idx = -1  # 存放DEC DEG的候选token idx
    # for token_idx, token in enumerate(obj_sentence.lst_tokens):
    #     # 如果循环到这个表述前面还没有找到那么就返回固定字符串
    #     if token.token_id > mention.lst_tokens[-1].token_id:
    #         return ConstantVariable.CONST_STRING_NO_MODIFIER
    #     # 这一步的目的是找到离表述最近的那个‘的地得’的相对位置
    #     if token.pos_info in ['DEC', 'DEG', 'DEV']:
    #         DEC_token_idx = token_idx
    #
    # if DEC_token_idx != -1:
    #     try:
    #         return obj_sentence.lst_tokens[DEC_token_idx + 1].word_itself
    #     except IndexError:
    #         return ConstantVariable.CONST_STRING_NO_MODIFIER

    # 3. 如果表述中含有 和 与表示并列的词语
    if u'和' in mention.chinese_word or \
        u'与' in mention.chinese_word:
        return mention.chinese_word

    # 4. 如果mention中 都是由NP组成，那么返回最后一个NP token
    if mention.lst_tokens[-1].pos_info in ['NN', 'NR', 'NT']:
        return mention.lst_tokens[-1].word_itself

    DEC_token_idx = -1  # 存放DEC DEG的候选token idx
    for token_idx, token in enumerate(obj_sentence.lst_tokens):
        # 如果循环到这个表述前面还没有找到那么就返回固定字符串
        if token.token_id > mention.lst_tokens[-1].token_id:
            return ConstantVariable.CONST_STRING_NO_MODIFIER
        # 这一步的目的是找到离表述最近的那个‘的地得’的相对位置
        if token.pos_info in ['DEC', 'DEG', 'DEV']:
            DEC_token_idx = token_idx

    if DEC_token_idx != -1:
        try:
            return obj_sentence.lst_tokens[DEC_token_idx + 1].word_itself
        except IndexError:
            return ConstantVariable.CONST_STRING_NO_MODIFIER



    return ConstantVariable.CONST_STRING_NO_MODIFIER
    #

def get_cluster(obj_document, mention):
    """
    根据mention的entity id，如果以E开头，说明有cluster了，返回obj_document.dic_entity[~]；否则返回[mention]
    返回以后需要多做一步类型检查
    """
    # if str(mention.entity_id).startswith('E_'):
    #     return obj_document.dic_entity.get(mention.entity_id, [mention])
    # return [mention]
    res = [mention]
    for m in obj_document.lst_mentions:
        if m.entity_id != -1 and m.entity_id == mention.entity_id:
            res.append(m)
    return res