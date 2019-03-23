# -*- coding: UTF-8 -*-
"""
只有满足各种约束的情况下才能设置cr
"""
import SubjectUtils.sieve_utils as sieve_util
from UserCorpus.api_user_corpus import get_stop_words
import ConstantVariable
import logging
import config
logger = logging.getLogger("sieve_strict_head_match_A")

@sieve_util.sieve_timer
def strict_head_matching_A(obj_document):
    for mention in obj_document.lst_mentions:
        if config.flag_jump_corefed_mention:
            if str(mention.entity_id).startswith('E_'):
                continue

        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        for candidate_m in candidate_mentions:
            candidate_m_entity = sieve_util.get_cluster(obj_document, candidate_m)
            # print candidate_m.chinese_word, ' | ', mention.chinese_word

            res_is_cluster_head_match = is_cluster_head_match(mention, candidate_m_entity)
            res_is_word_inclusion = is_word_inclusion(candidate_m, mention)
            res_is_compatible_modifier = is_compatible_modifier_only(obj_document, candidate_m, mention)
            res_is_i_within_i = is_i_within_i(candidate_m, mention)

            # logger.info("%s %s | %s %s %s %s"%
            #             (
            #                 mention.chinese_word,
            #                 candidate_m.chinese_word,
            #                 res_is_cluster_head_match,
            #                 res_is_word_inclusion,
            #                 res_is_compatible_modifier,
            #                 res_is_i_within_i
            #             )
            #             )

            if False not in {res_is_cluster_head_match, res_is_word_inclusion, res_is_compatible_modifier} and \
                res_is_i_within_i == False:
                obj_document.set_coref(candidate_m, mention)
                break
    return obj_document

def is_cluster_head_match(mention, lst_entity_mentions):
    """
    这个表述的先行词匹配在候选集合中任意的中心词。
    """
    for candidate_m_in_entity in lst_entity_mentions:
        if candidate_m_in_entity.head_word == mention.head_word:
            return True
    return False

def is_word_inclusion(candidate_mention, mention):
    """
    两个mention是否是互相包含
    :param candidate_mention:
    :param mention:
    :return:
    """
    candidate_words = set([i for i in candidate_mention.chinese_word if i not in get_stop_words()])
    mention_words = set([i for i in mention.chinese_word if i not in get_stop_words()])
    if candidate_words.issubset(mention_words) or mention_words.issubset(candidate_words):
        return True
    return False

def is_compatible_modifier_only(obj_document, candidate_mention, mention):
    """
    表述的修饰语都包含在候选先行词的修饰语中
    """
    sent_candidate = obj_document.dic_sentences.get(candidate_mention.sent_id)
    modifier_of_candidate_m = sieve_util.get_modifier(sent_candidate, candidate_mention)

    sent_m = obj_document.dic_sentences.get(mention.sent_id)
    modifier_of_m = sieve_util.get_modifier(sent_m, mention)

    if modifier_of_candidate_m == ConstantVariable.CONST_STRING_NO_MODIFIER or \
            modifier_of_m == ConstantVariable.CONST_STRING_NO_MODIFIER:
        return False

    if modifier_of_m in modifier_of_candidate_m:
        return True
    return False

def is_i_within_i(candidate_mention, mention):
    """
    判断是否是存在NP互相包含的情况，根据是否有相同的token判断
    """
    candidate_mention_tokens = candidate_mention.lst_tokens
    mention_tokens = mention.lst_tokens
    for token in candidate_mention_tokens:
        if token in mention_tokens:
            return True

    for token in mention_tokens:
        if token in candidate_mention_tokens:
            return True

    return False
