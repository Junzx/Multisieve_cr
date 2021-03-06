# -*- coding: UTF-8 -*-
from Multisieve.strict_head_matching_A import *
import SubjectUtils.sieve_utils as sieve_util
import logging
import config
logger = logging.getLogger("sieve_strict_head_match_B")

@sieve_util.sieve_timer
def strict_head_matching_B(obj_document):
    for mention in obj_document.lst_mentions:
        if config.flag_jump_corefed_mention:
            if str(mention.entity_id).startswith('E_'):
                continue

        # print '--------------'

        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        for candidate_m in candidate_mentions:
            candidate_m_entity = sieve_util.get_cluster(obj_document, candidate_m)
            # print candidate_m.chinese_word, ' | ', mention.chinese_word
            res_is_cluster_head_match = is_cluster_head_match(mention, candidate_m_entity)
            res_is_word_inclusion = is_word_inclusion(candidate_m, mention)
            res_is_i_within_i = is_i_within_i(candidate_m, mention)
            # print ': ', res_is_cluster_head_match, res_is_word_inclusion, res_is_i_within_i
            # logger.info("%s %s | %s %s %s"%
            #             (
            #                 mention.chinese_word,
            #                 candidate_m.chinese_word,
            #                 res_is_cluster_head_match,
            #                 res_is_word_inclusion,
            #                 res_is_i_within_i
            #             )
            #             )
            if False not in {res_is_cluster_head_match, res_is_word_inclusion} and \
                res_is_i_within_i == False:
                obj_document.set_coref(candidate_m, mention)
                break
    return obj_document