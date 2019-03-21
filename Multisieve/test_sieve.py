# -*- coding: UTF-8 -*-
from SubjectUtils.sieve_utils import sieve_timer
from SubjectUtils.sieve_utils import get_candidate_mentions
from SubjectUtils.sieve_utils import get_modifier
from SubjectUtils.sieve_utils import get_modifier_before
import ConstantVariable

@sieve_timer
def test_sieve(obj_document):

    # for mention in obj_document.lst_mentions:
    #     if mention.chinese_word in ConstantVariable.pronouns:
    #         continue
    #     #
    #
    #     sent_obj = obj_document.dic_sentences.get(mention.sent_id)
    #     print sent_obj.get_sent()
    #     modifier_today = get_modifier(sent_obj, mention)
    #     modifier_before = get_modifier_before(sent_obj, mention)
    #     print "表述： %s | 中心词： %s" % (mention.chinese_word, mention.head_word)
    #
    #     print "今天：%s | 之前： %s" % (modifier_today, modifier_before)
    #     print '---------------------'



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