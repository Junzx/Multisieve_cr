# -*- coding: UTF-8 -*-
from Multisieve.strict_head_matching_A import *
import SubjectUtils.sieve_utils as sieve_util
import logging
logger = logging.getLogger("multi_sieve")

def strict_head_matching_B(obj_document):
    for mention in obj_document.lst_mentions:
        print '--------------'

        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        for candidate_m in candidate_mentions:
            candidate_m_entity = sieve_util.get_cluster(obj_document, candidate_m)
            print candidate_m.chinese_word, ' | ', mention.chinese_word
            res_is_cluster_head_match = is_cluster_head_match(mention, candidate_m_entity)
            res_is_word_inclusion = is_word_inclusion(candidate_m, mention)
            res_is_i_within_i = is_i_within_i(candidate_m, mention)
            print ': ', res_is_cluster_head_match, res_is_word_inclusion, res_is_i_within_i
            if False not in {res_is_cluster_head_match, res_is_word_inclusion} and \
                res_is_i_within_i == False:
                obj_document.set_coref(candidate_m, mention)
    return obj_document