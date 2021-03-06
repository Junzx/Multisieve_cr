# -*- coding: UTF-8 -*-
"""
放cr过程中需要的函数

- get_candidate_mentions()  # 获取候选表述
- get_modifier()            # 获取mention的修饰语
"""
from math import fabs
import ConstantVariable
from time import clock
import logging
_time_logger = logging.getLogger("Sieve_Timer")
_modifier_logger = logging.getLogger("Modifier_INFO")

# 计算sieve用时
def sieve_timer(sieve_func):
    def run(*args):
        start = clock()
        result = sieve_func(*args)
        end = clock()
        _time_logger.info("%s 用时: %.5f s\n" % (sieve_func.__name__, end - start))
        return result
    run.__name__ = sieve_func.__name__
    return run


def word_similiar(word1, word2):
    return 0.8

def get_candidate_mentions_old(obj_document, obj_mention):
    """
    旧方法，做对比实验用
    """
    sentence_distance = 100  # 表示 表述所在的句子，以及之前的 n 个句子
    if obj_mention.mention_id == 0:
        return []
    candidate_mentions = []
    sent_id = obj_mention.sent_id
    mention_id = obj_mention.mention_id
    for candidate_m in obj_document.lst_mentions:
        # if str(candidate_m.entity_id).startswith('E_'):
        #     continue

        # 如果是代词则跳过去
        if candidate_m.chinese_word in ConstantVariable.pronouns:
            continue

        if candidate_m.sent_id <= sent_id and \
                fabs(candidate_m.sent_id - sent_id) <= sentence_distance and \
                candidate_m.mention_id != mention_id:
            candidate_mentions.append(candidate_m)

        elif candidate_m.mention_id == mention_id or candidate_m.sent_id > sent_id:
            break
    return candidate_mentions

def get_candidate_mentions(obj_document, obj_mention):
    """
    给定mention并返回候选表述
    目前实现：
        1. 获取mention的句子id
        2. 获取前n=3个sent对象（包括当前表述所在的句子）
        3. 从后向前选择sent对象，其中表述按照从左向右选取

    update： 跳过代词
    """
    # 找到前n个句子obj
    sent_lst = []
    sentence_distance = 5  # 表示 表述所在的句子，以及之前的 n 个句子
    the_sent_id = obj_mention.sent_id
    for sent_id, sent in obj_document.dic_sentences.items():
        if sent_id <= the_sent_id and \
                fabs(sent_id - the_sent_id) <= sentence_distance:
            sent_lst.append(sent)
        elif sent_id > the_sent_id:
            break

    lst_candidate_mentions = []
    for sent in reversed(sent_lst):
        for mention in sent.lst_mentions:
            if mention.mention_id < obj_mention.mention_id and \
                    mention.chinese_word not in ConstantVariable.pronouns:
                lst_candidate_mentions.append(mention)

    return lst_candidate_mentions


def get_modifier_before(obj_sentence, mention):
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



def get_modifier(obj_sentence, mention):
    """
    获取修饰语
    方法：
    1. 检查是否有 的地得，如果有，返回前面的部分
    2. 如果没有的地得，那么找ADJP。返回这个token.word_itself
    3. 如果都没有，判断包含表述的句子中是否有的
    """
    # 1. 先检查mention中是否有 ‘的地得’
    de_token_idx = -1
    for token_idx, token in enumerate(mention.lst_tokens):
        if token.pos_info in ['DEC', 'DEG', 'DEV']:    # 是 的地得
            de_token_idx = token_idx

    if de_token_idx != -1:
        return ''.join([t.word_itself for t in mention.lst_tokens[:de_token_idx]])


    # 2. 检查ADJP
    modifier_word = ''
    for t in mention.lst_tokens:
        if 'ADJP' in t.parse_info:
            modifier_word += t.word_itself
    if modifier_word != '':
        return modifier_word

    # ===============3 针对Mention在句子中的位置=================
    # 整个句子： 佩雷斯 / 说 /： / “ / 中国 / 和 / 以色列 / 地处 / 亚洲 / 的 / 两 / 端 /， / 相隔 / 万水千山 /。
    # 切割的： 佩雷斯 / 说 /： / “ / 中国 / 和 / 以色列 / 地处 / 亚洲 / 的 / 两
    # 原始Mention: 端
    # -------
    # 这个是个的： 亚洲
    # NR(NP(DNP(NP *)
    # res: 端
    # 亚洲
    # 在Mention前面的所有token（句子中）
    token_before_mention = []
    for t in obj_sentence.lst_tokens:
        if t.token_id < mention.lst_tokens[0].token_id:
            token_before_mention.append(t)

    # 找到Mention前面的一个“的”，如果挨着近，那么就是modifier
    de_token = None
    for token_idx, token in enumerate(token_before_mention):
        if token.pos_info in ['DEC', 'DEG', 'DEV']:    # 是 的地得
            de_token = token

    if de_token != None:
        if fabs(de_token.token_id - mention.start_token_id) < 3:
            modifier_token = obj_sentence.lst_tokens[int(str(de_token.word_id).encode('utf-8')) - 1]
            # if 'VP' not in modifier_token.parse_info:
            return modifier_token.word_itself


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


def is_numeric_mismatches(candidate_mention,mention):
    """
    第二个表述不能有再先行词中没出现的数字（people / around 200 people）
    :return:如果满足以上条件返回true；否则返回False
    """
    the_word = the_candidate_word = 'No'
    if u'百' in mention.chinese_word or \
        u'千' in mention.chinese_word or \
        u'万' in mention.chinese_word or \
        u'亿' in mention.chinese_word:
        number = [u'百',u'千',u'万',u'亿']
        number.extend(list(u'1234567890'))
        for token in mention.lst_tokens:
            # if token.word_itself in [u'百',u'千',u'万',u'亿'].extend(list(u'1234567890')):
            if token.word_itself in number:
                the_word = token.word_itself
        if u'百' in candidate_mention.chinese_word or \
            u'千' in candidate_mention.chinese_word or \
            u'万' in candidate_mention.chinese_word or \
            u'亿' in candidate_mention.chinese_word:
            for token in candidate_mention.lst_tokens:
                # if token.word_itself in [u'百',u'千',u'万',u'亿'].extend(list('1234567890')):
                if token.word_itself in number:
                    the_candidate_word = token.word_itself

            if the_word == the_candidate_word and the_word != 'No' and the_candidate_word != 'No':
                return False
    return True
