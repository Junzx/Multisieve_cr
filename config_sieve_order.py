# coding: utf-8


# ---------- 7 pass -------------
from Multisieve.test_sieve import test_sieve
from Multisieve.exact_match import exact_match
from Multisieve.precise_constructs import precise_constructs
from Multisieve.strict_head_matching_A import strict_head_matching_A
from Multisieve.strict_head_matching_B import strict_head_matching_B
from Multisieve.strict_head_matching_C import strict_head_matching_C
from Multisieve.relaxing_head_matching import relaxing_head_matching
from Multisieve.pronounce_cr import pronoun_sieve
# ------
from Multisieve.discourse_processing import discourse_processing
from Multisieve.proper_head_word_match import proper_header_word_match_sieve
from Multisieve.other_sieve import other_sieve
from Multisieve.final_sieve import filter_sieve

# 我的顺序
sieve_order = [
        test_sieve,
        exact_match,
        strict_head_matching_A,
        strict_head_matching_B,
        strict_head_matching_C,
        proper_header_word_match_sieve,
        # precise_constructs,
        # relaxing_head_matching,
        discourse_processing,
        pronoun_sieve,
        other_sieve,
        filter_sieve,
    ]