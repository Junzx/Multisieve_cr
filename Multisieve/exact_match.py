# -*- coding: UTF-8 -*-
"""
Exact Match
This model links two mentions only if they contain exactly the same extent text,
including modifiers and determiners, e.g., the Sha 3 ground-ground missile.
As expected, this model is extremely precise, with a pairwise precision over 96%.
如果两个表述的修饰语和限定词相同，说明共指

函数逻辑：
    如果两个表述的修饰语和限定词均相同，且不是默认值，则两个表述共指
"""
import logging
import ConstantVariable
import SubjectUtils.sieve_utils as sieve_util
logger = logging.getLogger("multi_sieve")

def exact_match(obj_document):

    for mention in obj_document.lst_mentions:
        candidate_mentions = sieve_util.get_candidate_mentions(obj_document, mention)
        modifier_this_mention = sieve_util.get_modifier(mention)
        determiner_this_mention = sieve_util.get_determiner(mention)
        for candidate_m in candidate_mentions:
            modifier_candidate_mention = sieve_util.get_modifier(candidate_m)
            determiner_candidate_mention = sieve_util.get_determiner(candidate_m)

            if modifier_candidate_mention == modifier_this_mention and \
                ConstantVariable.CONST_STRING_NO_MODIFIER not in (modifier_this_mention, modifier_candidate_mention):
                if determiner_candidate_mention == determiner_this_mention and \
                    ConstantVariable.CONST_STRING_NO_DETERMINER not in (determiner_this_mention, determiner_candidate_mention):
                    obj_document.set_coref(candidate_m, mention)

    return obj_document