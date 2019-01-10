# -*- coding: UTF-8 -*-
"""
如果以下条件被任意满足一个，那么两个表述共指
"""
from math import fabs
import SubjectUtils.sieve_utils as sieve_util
from UserCorpus.api_user_corpus import get_abbreviation_dict, get_nation, get_adj_nation
import ConstantVariable
import logging
logger = logging.getLogger("multi_sieve")

def precise_constructs(obj_document):
    for mention in obj_document.lst_mentions:
        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        for candidate_m in candidate_mentions:
            # 如果两个表述在同一个句子中才可能是同位语关系
            if mention.sent_id == candidate_m.sent_id:
                tmp_sent_obj = obj_document.dic_sentences[mention.sent_id]
                res_is_appositive = is_appositive(tmp_sent_obj, candidate_m, mention)   # 是否为同位语
                res_is_predicate_ = is_predicate_nominative(tmp_sent_obj, candidate_m, mention) # 是否为谓语主格
                res_is_role_ = is_role_appositive(candidate_m, mention)    # 是否为角色同位语
                res_is_acronym = is_acronym(candidate_m, mention)           #
                res_is_demonym = is_demonym(candidate_m, mention)

                if True in {res_is_predicate_, res_is_role_, res_is_acronym, res_is_demonym}:
                    obj_document.set_coref(candidate_m, mention)
            else:
                continue

    return obj_document

def is_appositive(obj_sentence, candidate_mention, mention):
    """
    判断两个mention是否处于同位语结构
    (NP
    (NP (NR 中国))
    (NP (NN 首都))))
    :return:如果是同位语结构，返回True；如果不是，返回false
    """

    # 1. 首先 两个表述距离比较近
    if fabs(candidate_mention.mention_id - mention.mention_id) < 3:
        # 如果有逗号分割，判断为松散同位语
        candidate_m_end_token_idx = candidate_mention.lst_tokens[-1].token_id
        mention_start_token_idx = mention.lst_tokens[0].token_id
        tmp_lst = []    # 临时存放两个表述之间的token obj
        for token in obj_sentence.lst_tokens:
            if candidate_m_end_token_idx <= token.token_id <= mention_start_token_idx:
                tmp_lst.append(token)

        # 若中间有token
        if tmp_lst:
            # 如果有逗号，且两个表述距离不远
            for t in tmp_lst:
                if t.word_itself in ConstantVariable.comma and \
                        mention_start_token_idx - candidate_m_end_token_idx < 5:
                    return True
    return False
            # 如果没有逗号，判断是否为紧密型同位语，要求表述必须是由一个token构成的
            # 以下是僵尸代码，没有实现，主要功能是识别紧密性同位语结构
            # if len(candidate_mention.lst_tokens) == len(mention.lst_tokens) == 1:
            #     word_sim = sieve_util.word_similiar(candidate_mention.chinese_word, mention.chinese_word)
            #     parse_candidate_mention = candidate_mention.parse
            #     parse_mention = mention.parse
            #     parse_string = obj_sentence.get_sent_parse()
            #     tree = Tree.fromstring(parse_string)
            #     candidate_token = candidate_mention.lst_tokens[0]
            #     token = mention.lst_tokens[0]
            #     candidate_token_tree = Tree.fromstring(candidate_token.parse_info)
            #     token_tree = Tree.fromstring(token.parse_info)

def is_predicate_nominative(obj_sentence, candidate_mention, mention):
    """
    谓语主格，这里主要判断是否是mention1 is mention2
    """
    if mention.mention_id - candidate_mention.mention_id < 8:
        # 如果有逗号分割，判断为松散同位语
        candidate_m_end_token_idx = candidate_mention.lst_tokens[-1].token_id
        mention_start_token_idx = mention.lst_tokens[0].token_id
        tmp_lst = []    # 临时存放两个表述之间的token obj
        for token in obj_sentence.lst_tokens:
            if candidate_m_end_token_idx <= token.token_id <= mention_start_token_idx:
                tmp_lst.append(token)

        if tmp_lst:
            for t in tmp_lst:
                if t.word_itself in ConstantVariable.word_bag_is:   # 有 ‘是’
                    return True
    return False

def is_role_appositive(candidate_mention, mention):
    """
    1. 表述被标记为PERSON
    2. 先行词是animate
    3. 先行词的性别不是中性
    """
    if mention.ner == 'PERSON' and \
        candidate_mention.animacy == 1 and \
        candidate_mention.gender != 0:
        return True
    return False

def is_acronym(candidate_mention, mention):
    """
    判断两个表述是否具有缩写的关系
    """
    tmp_candidate_m = get_abbreviation_dict().get(candidate_mention.chinese_word, 'NO')
    tmp_m = get_abbreviation_dict().get(mention.chinese_word, "NO")

    if mention.chinese_word == tmp_candidate_m or \
        candidate_mention.chinese_word == tmp_m:
        return True
    return False

def is_demonym(candidate_mention, mention):
    """
    Demonym-区域居民称谓词
    一个表述是另一个表述的～，比如 美国 = 美国人
    """
    if (candidate_mention.chinese_word in get_nation() and
            mention.chinese_word in get_adj_nation()) or \
        (mention.chinese_word in get_nation() and
            candidate_mention.chinese_word in get_adj_nation()):
        return True
    return False

