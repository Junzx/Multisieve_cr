# -*- coding: UTF-8 -*-
from SubjectUtils.sieve_utils import sieve_timer
from SubjectUtils.sieve_utils import get_candidate_mentions
from SubjectUtils.sieve_utils import get_modifier
import ConstantVariable

@sieve_timer
def test_sieve(obj_document):

    # for mention in obj_document.lst_mentions:
    #     if mention.chinese_word in ConstantVariable.pronouns:
    #         continue

        # print mention.chinese_word, mention.head_word

        # ----------------------------------------
        # -----------------测试候选表述---------------
        # ----------------------------------------
        # candidate_ms = get_candidate_mentions(obj_document, mention)
        # print mention.chinese_word,mention.mention_id,mention.sent_id
        # print
        # for candidate_m in candidate_ms:
        #     print '候选：',candidate_m.chinese_word, candidate_m.mention_id, candidate_m.sent_id
        # print '=-==-=-=-=-=-=--=-=-=-='

        # ----------------------------------------
        # ----------------测试修饰语-----------------
        # ----------------------------------------
        # print '-=' * 60
        # modifier = get_modifier(obj_document.dic_sentences.get(mention.sent_id), mention)
        # print 'res:', mention.chinese_word, modifier, obj_document.dic_sentences.get(mention.sent_id).get_sent()
    return obj_document