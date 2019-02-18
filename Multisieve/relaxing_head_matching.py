# -*- coding: UTF-8 -*-
"""
表述的中心词可以匹配任何候选先行词所在的cluster中的词语
要求表述和候选先行词被标记为同样的命名实体（同类）
word inclusion
not i-within-i
"""
import strict_head_matching_A
import SubjectUtils.sieve_utils as sieve_util

def relaxing_head_matching(obj_document):
    for mention in obj_document.lst_mentions:
        if str(mention.entity_id).startswith('E_'):
            continue

        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        # print '------------'
        for candidate_m in candidate_mentions:

            # print candidate_m.chinese_word, mention.chinese_word
            candidate_mention_entity = sieve_util.get_cluster(obj_document, mention)
            res_is_head_relax_match = False
            res_is_same_ner = False
            for tmp_m in candidate_mention_entity:
                if tmp_m.head_word == mention.head_word:
                    res_is_head_relax_match = True
                if tmp_m.ner == mention.ner:
                    res_is_same_ner = True
            res_is_word_clusion = strict_head_matching_A.is_word_inclusion(candidate_m, mention)
            res_is_i_within_i = strict_head_matching_A.is_i_within_i(candidate_m, mention)
            # print res_is_head_relax_match, res_is_same_ner, res_is_word_clusion, res_is_i_within_i
            if False not in {res_is_head_relax_match, res_is_same_ner, res_is_word_clusion} and \
                    not res_is_i_within_i:
                obj_document.set_coref(candidate_m, mention)


    return obj_document