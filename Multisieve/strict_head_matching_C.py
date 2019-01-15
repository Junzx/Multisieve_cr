# -*- coding: UTF-8 -*-
from Multisieve.strict_head_matching_A import *
import SubjectUtils.sieve_utils as sieve_util
import logging
logger = logging.getLogger("multi_sieve")

def strict_head_matching_C(obj_document):
    for mention in obj_document.lst_mentions:
        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        for candidate_m in candidate_mentions:
            candidate_m_entity = sieve_util.get_cluster(obj_document, candidate_m)
            res_is_cluster_head_match = is_cluster_head_match(mention, candidate_m_entity)
            res_is_compatible_modifier = is_compatible_modifier_only(obj_document, candidate_m, mention)
            res_is_i_within_i = is_i_within_i(candidate_m, mention)

            if False not in {res_is_cluster_head_match, res_is_compatible_modifier} and \
                res_is_i_within_i == False:
                obj_document.set_coref(candidate_m, mention)
    return obj_document