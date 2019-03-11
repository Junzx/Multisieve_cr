# -*- coding: UTF-8 -*-
from math import fabs
from SubjectUtils.get_similarity.word_similarity import get_similarity_API

def other_sieve(obj_document):
    """
    自己凭借经验找的关系
    """
    '''
    lst_no_core_mentions = [m for m in obj_document.lst_mentions if not str(m.entity_id).startswith('E_')]

    # log_CR_cmn_0029_001,解决你\我
    for index_mention,mention in enumerate(obj_document.lst_mentions):
        if mention.chinese_word == '我' and not str(mention.entity_id).startswith('E_'):
            # 由于是代词,获取候选表述的方式如下
            lst_candidate_mention = [m for m in obj_document.lst_mentions[:index_mention] if m.chinese_word == '我']
            for index_candidate_mention,candidate_mention in enumerate(lst_candidate_mention):
                if mention.sent_id - candidate_mention.sent_id <= 3:
                    obj_document.set_coref(candidate_mention,mention)
        if mention.chinese_word == '你' and not str(mention.entity_id).startswith('E_'):
            # 由于是代词,获取候选表述的方式如下
            lst_candidate_mention = [m for m in obj_document.lst_mentions[:index_mention] if m.chinese_word == '你']
            for index_candidate_mention,candidate_mention in enumerate(lst_candidate_mention):
                if mention.sent_id - candidate_mention.sent_id <= 3:
                    obj_document.set_coref(candidate_mention,mention)
        if mention.chinese_word == '我们' and not str(mention.entity_id).startswith('E_'):
            # 由于是代词,获取候选表述的方式如下
            lst_candidate_mention = [m for m in obj_document.lst_mentions[:index_mention] if m.chinese_word == '我们']
            for index_candidate_mention,candidate_mention in enumerate(lst_candidate_mention):
                if mention.sent_id - candidate_mention.sent_id <= 3:
                    obj_document.set_coref(candidate_mention,mention)
    # 解决未处理的代词问题
    # for mention in self.obj_document.lst_mentions:
    for mention in lst_no_core_mentions:
        # 处理代词
        if mention.chinese_word in ['她','他','其','他们','她们']:
            if mention.mention_id - 1 > 1:
                obj_document.set_coref(obj_document.lst_mentions[mention.mention_id - 1], mention)
    '''

    lst_no_core_mentions = [m for m in obj_document.lst_mentions if not str(m.entity_id).startswith('E_')]
    # 解决未处理的 a in b问题
    for index_mention, mention in enumerate(lst_no_core_mentions):
        if index_mention == 0:
            continue

        lst_candidate_mention = lst_no_core_mentions[:index_mention]
        for candidate_mention in lst_candidate_mention:
            if (mention.chinese_word in candidate_mention.chinese_word or
                candidate_mention.chinese_word in mention.chinese_word) and \
                    candidate_mention.head_word == mention.head_word and \
                    fabs(mention.sent_id - candidate_mention.sent_id) < 2:
                obj_document.set_coref(candidate_mention, mention)


    # lst_no_core_mentions = [m for m in obj_document.lst_mentions if not str(m.entity_id).startswith('E_')]
    # if len(lst_no_core_mentions) >= 2:
    #     for index_mention, mention in enumerate(lst_no_core_mentions):
    #         if index_mention == 0:
    #             continue
    #         if get_similarity_API(
    #                 lst_no_core_mentions[index_mention - 1].chinese_word, mention.chinese_word) > 0.6:
    #             obj_document.set_coref(lst_no_core_mentions[index_mention - 1], mention)
    #             break

    return obj_document