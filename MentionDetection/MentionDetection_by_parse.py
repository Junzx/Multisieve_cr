# coding: utf-8
"""
通过句法树信息提取表述
方法：
    1. load conll
"""
from nltk import Tree
from copy import deepcopy
from LoadConll import load_one_file,load_one_file_for_md
from ClassDefinition.Definition_Sentence import Sentence
from ClassDefinition.Definition_Mention import Mention
import SubjectUtils.mention_detection_utils as mention_detection_utils
import exact_np_by_tree
import ConstantVariable


# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ================================== 以 下 是 新 的 方 法 ============================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================

def Mention_Detection(obj_document):
    """
    MD主程序
    以句子为单位，提取表述
    """
    dic_sentence = {}
    obj_document.lst_mentions = []
    obj_document.dic_mentions = {}
    obj_document.dic_entity = {}

    # 根据token list构建sent对象
    sent_id = 0
    sent_lst_tokens = []
    # 以句子为单位创建sentence对象并提取表述
    for token in obj_document.lst_tokens:
        if token.sent_id == sent_id:
            sent_lst_tokens.append(token)

        if token.sent_id != sent_id:
            obj_sentence = init_sentence_object(lst_tokens=sent_lst_tokens)
            dic_sentence.setdefault(sent_id, obj_sentence)
            sent_id += 1    # 更新sent id
            del sent_lst_tokens[:]
            sent_lst_tokens.append(token)

            for mention in obj_sentence.lst_mentions:
                obj_document.lst_mentions.append(mention)

    # 有的document可能就有一句话
    if sent_lst_tokens != []:
        obj_sentence = init_sentence_object(lst_tokens=sent_lst_tokens)
        dic_sentence.setdefault(sent_id, obj_sentence)
        sent_id += 1  # 更新sent id
        del sent_lst_tokens[:]
        sent_lst_tokens.append(token)

        for mention in obj_sentence.lst_mentions:
            obj_document.lst_mentions.append(mention)

    obj_document.dic_sentences = dic_sentence
    for m in obj_document.lst_mentions:
        obj_document.dic_mentions.setdefault(m.mention_id, m)
    return obj_document

def init_sentence_object(lst_tokens):
    obj_sentence = Sentence()
    obj_sentence.sent_id = lst_tokens[0].sent_id
    for token in lst_tokens:
        obj_sentence.lst_tokens.append(token)

    # parse tree
    lst_mentions_from_parse = extract_mention_from_sentence(obj_sentence)  # 提取sent对象中的表述
    for m in lst_mentions_from_parse:
        obj_sentence.lst_mentions.append(m)

    # ner
    # obj_sentence = extract_named_entity(obj_sentence)

    # 代词
    # obj_sentence = extract_pronoun(obj_sentence)

    # 过滤器
    # obj_sentence = mention_filter(obj_sentence)

    return obj_sentence

def extract_mention_from_sentence(obj_sentence):
    """
    接受一个句子，抽取Mention
    :param obj_sentence:
    :return: obj_sentence, lst_mentions
    """
    # 根据句法树提取
    composition = 'NP'
    str_sentence = mention_detection_utils.make_to_sentence(obj_sentence.lst_tokens)  # 构成一句话
    composition = mention_detection_utils.exact_composition(str_sentence, composition)  # 抽取NP
    num_composition = mention_detection_utils.exact_word(composition)
    obj_sentence = set_mention_info(obj_sentence, num_composition)
    lst_mentions = exact_np_by_tree.extract_mention(obj_sentence.lst_tokens)

    return lst_mentions

def set_mention_info(obj_sentence, lst_all_num_composition):
    """
    设置mention中的每个token的npinfo
    2018年2月28日
    """
    # 例如：lst_all_candidate_mention = [(0, 0), (1, 1), (5, 5), (8, 9), (9, 9)]
    for index_mention,tup_candidate_mention in enumerate(lst_all_num_composition):
        int_first_token_id = tup_candidate_mention[0]
        int_second_token_id = tup_candidate_mention[1]

        if int_first_token_id == int_second_token_id:    # （9，9） 两个相等
            str_new_np_info = '(' + str(index_mention) + ')'
            __add_np_info(obj_sentence.get_token_by_id(int_first_token_id),str_new_np_info)

        elif int_first_token_id != int_second_token_id:  # （8，10）两个不等
            obj_start_token = obj_sentence.get_token_by_id(int_first_token_id)
            obj_end_token = obj_sentence.get_token_by_id(int_second_token_id)

            str_start_token_info = '(' + str(index_mention)
            str_end_token_info = str(index_mention) + ')'

            __add_np_info(obj_start_token,str_start_token_info)
            __add_np_info(obj_end_token,str_end_token_info)
    return obj_sentence

def __add_np_info( token, new_np_info):
    if token.np_info == '-':
        token.np_info = str(new_np_info)
    else:
        if '(' in token.np_info:
            token.np_info = token.np_info + '|' + new_np_info
        elif ')' in token.np_info:
            token.np_info = new_np_info + '|' + token.np_info

# ================================================================
def extract_named_entity(obj_sentence):

    mention_id = len(obj_sentence.lst_mentions)
    entity_id = len(obj_sentence.lst_mentions)

    tmp_ner_tokens = []
    flag_new_mention = False

    now_mention_list = [(m.lst_tokens[0].token_id, m.lst_tokens[0].token_id)
                        for m in obj_sentence.lst_mentions]

    for token in obj_sentence.lst_tokens:
        if '(' in token.original_ner and ')' not in token.original_ner:   # （（DATA ----）的形式
            tmp_ner_tokens.append(token)
        elif '(' not in token.original_ner and ')' in token.original_ner: # 接上，是闭合的括号
            tmp_ner_tokens.append(token)
            flag_new_mention = True
        elif '(' in token.original_ner and ')' in token.original_ner: # （ORG）
            tmp_ner_tokens.append(token)
            flag_new_mention = True

        if flag_new_mention:
            # 检查这个idx范围是否出现在已有的表述中
            tmp = (tmp_ner_tokens[0].token_id, tmp_ner_tokens[-1].token_id)
            if tmp in now_mention_list:
                continue

            # 以下说明没有，将新建一个表述
            obj_mention = Mention()
            obj_mention.mention_id = mention_id
            obj_mention.entity_id = entity_id
            for t in tmp_ner_tokens:
                obj_mention.lst_tokens.append(t)

            obj_mention.set_other_attributes(obj_mention.lst_tokens)

            obj_sentence.lst_mentions.append(obj_mention)

            mention_id += 1
            entity_id += 1

            flag_new_mention = False
            del tmp_ner_tokens[:]   # 清空
    return obj_sentence

def extract_pronoun(obj_sentence):
    mention_id = len(obj_sentence.lst_mentions)
    entity_id = len(obj_sentence.lst_mentions)
    for token in obj_sentence.lst_tokens:
        if token.word_itself in ConstantVariable.pronouns:
            obj_mention = Mention()
            obj_mention.mention_id = mention_id
            obj_mention.entity_id = entity_id
            obj_mention.lst_tokens.append(token)

            obj_mention.set_other_attributes(obj_mention.lst_tokens)
            obj_sentence.lst_mentions.append(obj_mention)

            mention_id += 1
            entity_id += 1

            # obj_sentence.lst_mentions.append(deepcopy(obj_mention))
    return obj_sentence

def mention_filter(obj_sentence):
    # 待删除的表述的Mention id
    del_mention_idx = []

    # 规则1 删停用词
    stop_word = ConstantVariable.corpus_dict.get('stop_word')
    verb_word = ConstantVariable.corpus_dict.get('verb')
    for mention in obj_sentence.lst_mentions:
        if mention.chinese_word in stop_word:
            del_mention_idx.append(mention.mention_id)

        if 'NP' not in mention.parse:
            del_mention_idx.append(mention.mention_id)

        if 'QP' in mention.parse:
            del_mention_idx.append(mention.mention_id)
        parse_item = [pos for pos in mention.parse.replace('(', ' ').replace(')', ' ').replace('*', ' ').split(' ') if
                  pos != '']

        if len(mention.lst_tokens) == 1 and 'ADJP' in parse_item:
            del_mention_idx.append(mention.mention_id)

        if len(parse_item) > 5:
            if 'NP' in parse_item and len(parse_item) > 0:
                if 0.90 < parse_item.count('NP') / len(parse_item) < 1.0:
                    del_mention_idx.append(mention.mention_id)

        if mention.chinese_word in verb_word:
            del_mention_idx.append(mention.mention_id)

    # 删除相同的
    mention_t_idx = []
    for mention in obj_sentence.lst_mentions:
        tmp = (mention.lst_tokens[0].token_id, mention.lst_tokens[-1].token_id)
        if tmp not in mention_t_idx:
            mention_t_idx.append(tmp)
        else:
            del_mention_idx.append(mention.mention_id)

    # 根据list删除Mention
    tmp_mentions = []
    for mention in obj_sentence.lst_mentions:
        if mention.mention_id not in del_mention_idx:
            tmp_mentions.append(mention)

    del obj_sentence.lst_mentions[:]
    for mention in tmp_mentions:
        obj_sentence.lst_mentions.append(mention)
    return obj_sentence



def __unit_test():
    from pprint import pprint
    data = load_one_file_for_md('test.v4_gold_conll')
    res_data = Mention_Detection(data)
    # name_eneity = extract_named_entity(data)
    print len(res_data.lst_mentions)
    # for mention in res_data.lst_mentions:
    #     pprint(mention.__dict__)
    #     print '--------------------'
    # print 'shit'

if __name__ == '__main__':
    __unit_test()
