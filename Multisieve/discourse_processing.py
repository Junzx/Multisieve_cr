# -*- coding: UTF-8 -*-
import ConstantVariable

def discourse_processing(obj_document):
    """
    这个函数目前处理第一二人称
    """

    # 遍历所有表述，找到定义为speaker的表述
    report_verbs = ConstantVariable.speak_verbs_set

    # 找report verb
    lst_report_token_index = []  # 放report verb的token的index
    for token in obj_document.lst_tokens:
        # print token.word_itself
        if token.word_itself in report_verbs:
            lst_report_token_index.append(token.token_id)

    # 找speaker
    lst_speaker_mention_id = []  # 存放mention id
    for mention in obj_document.lst_mentions:
        for report_verb_index in lst_report_token_index:
            if 0 < (mention.end_token_id - obj_document.get_token_by_id(report_verb_index).token_id) < 10:
                # print self.obj_document.get_token_by_id(mention.end_token_id).word_itself,self.obj_document.get_token_by_id(report_verb_index).token_id,self.obj_document.get_token_by_id(report_verb_index).word_itself
                lst_speaker_mention_id.append(mention.mention_id)

    # 考虑所有的代词与speaker的关系
    for mention_speaker_id in lst_speaker_mention_id:
        mention_speaker = obj_document.get_mention_by_id(mention_speaker_id)
        for mention in obj_document.lst_mentions:
            # 这里只考虑第一二三人称代词
            if mention.pos_info != 'PN':
                continue

            mention_candidate_id = mention.mention_id
            # 如果是第一人称
            if mention.chinese_word in ConstantVariable.first_person_pronouns:
                # 句子距离小于2、表述指代前一个speaker
                if 0 < mention_speaker.sent_id - mention.sent_id < 2:
                    # 如果符合条件 将代词指向speaker
                    obj_document.set_coref(mention_speaker_id, mention_candidate_id)

            # 如果是第二人称
            if mention.chinese_word in ConstantVariable.second_person_pronouns:
                # 句子距离小于4、表述指代后一个speaker
                if 0 < mention.sent_id - mention_speaker.sent_id < 4:
                    # 如果符合条件 将代词指向speaker
                    obj_document.set_coref(mention_candidate_id, mention_speaker_id)

    return obj_document
