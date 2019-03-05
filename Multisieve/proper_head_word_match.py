# -*- coding: UTF-8 -*-
from strict_head_matching_A import is_i_within_i
from SubjectUtils.sieve_utils import is_numeric_mismatches
import SubjectUtils.sieve_utils as sieve_util

def proper_header_word_match_sieve(obj_document):
    """
    考虑两个中心词是专有名词的表述，如果它们的中心词相同且满足以下约束
    1. Not i-within-i
    2. 非地点不匹配：两个表述的修饰语不能包括不同的地点实体、其他的专有名词、空间修饰语
    3. 非数量不匹配：第二个表述不能有再先行词中没出现的数字（people / around 200 people）
    """
    for index_mention, mention in enumerate(obj_document.lst_mentions):
        if str(mention.entity_id).startswith('E_'):
            continue

        if index_mention == 0:
            continue
        if mention.get_head_word_token_ner() == '-':
            continue

        lst_candidate = sieve_util.get_candidate_mentions(obj_document, mention)  # 获取候选表述list
        for candidate_mention in lst_candidate:
            if candidate_mention.get_head_word_token_ner() == '-':
                continue

            # TODO:剩下的两个条件（2）
            if candidate_mention.head_word == mention.head_word and \
                    not is_i_within_i(candidate_mention, mention) and \
                    is_numeric_mismatches(candidate_mention, mention):
                obj_document.set_coref(candidate_mention, mention)
                break
                # print candidate_mention.chinese_word,mention.chinese_word
    return obj_document