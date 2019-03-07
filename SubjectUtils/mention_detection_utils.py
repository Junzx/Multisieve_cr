# coding: utf-8
"""
专用于MD
"""
from copy import deepcopy
from nltk import Tree

def make_to_sentence(lst_tokens):
    """
    测试用，将句法信息合成为一句话
    返回类似于：        (TOP(IP(NP(NP0) (NP1)) (VP(ADVP2) (PP3 (NP(DP4) (NP5))) (VP6 7 (NP8))) 9))
    """
    str_sentence = ''
    for token in lst_tokens:
        syntax = token.parse_info
        # str_sentence += syntax.replace('*', obj_iter_token.word_id)         # 用word id替换*
        str_sentence += syntax.replace('*', ' ' + str(token.token_id))  # test，用token id替换*
        str_sentence += ' '
    return str_sentence

def exact_composition(str_sentence, composition):
    """
    输入的str_sentence类似于：
    (TOP(IP(NP(NP0) (NP1 2) (NP3 4)) 5 (VP6 (IP(VP(PP7 (NP(CP(IP(VP8 (NP(NP9 10) (ADJP11) (NP12))))) (NP13 14 15))) (VP16 (NP17))))) 18))
    (TOP(IP(IP(NP0) (VP1 (NP2) (IP(VP3 (NP(DNP(PP4 (NP5)) 6) (NP7)))))) 8 (IP(VP9 (IP(NP(QP10 (CLP11)) (NP12)) (VP(PP13 (LCP(NP(DP14 (CLP15)) (NP16)) 17)) (VP18))))) 19))
    (TOP(IP(NP(QP0) (NP1) (NP2)) (VP(PP3 (IP(VP(ADVP4) (VP5 (NP6))))) (VP7 (NP8))) 9))
    (TOP(IP(NP(NP0) (NP1)) (VP(ADVP2) (PP3 (NP(DP4) (NP5))) (VP6 7 (NP8))) 9))
    (TOP(IP(NP0) (NP(NP(NP(NP1) (NP2)) (NP3)) 4 (NP(NP5 6 7) (NP8))) 9 (VP(PP10 (NP(CP(CP(IP(NP11) (VP(PP12 (NP13 14)) (VP15))) 16)) (NP17))) (VP18 (NP19))) 20))
    composition:为要筛选出的类型，包括：['(TOP','(CP','(NP','(ADJP','(DP','(VP','(PP','(ADVP','(QP','(IP','(CLP','(LCP']
    返回一个list
    """
    # print str_sentence, composition
    lst_result = [] # 放结果的

    tree_sent = Tree.fromstring(str_sentence)   # 构建树结构
    for tree_iter_sub in tree_sent.subtrees():
        if str(tree_iter_sub).startswith('(' + composition):
            lst_result.append(str(tree_iter_sub))

    # print lst_result
    return lst_result

def exact_word(lst_var):
    """
    给定一个list，依次迭代里面的元素，然后根据id组合成中文
    返回一个包含中文的list
    ['0/1/2/', '1/', '2/', '6/', '8/']
    """
    lst_result = [] # 放结果的
    for str_iter in lst_var:

        tmp_num = ''
        for index_char, char_iter in enumerate(str_iter):
            # 对每个char字符进行迭代处理
            flag = False

            if char_iter in '0123456789':   # 首先必须是数字
                tmp_num += char_iter

                # 检查下一位是否是数字
                if str_iter[index_char + 1] in '0123456789':
                    flag = True

                # 如果不是数字则加上分隔符
                if not flag:
                    tmp_num += '/'  # 分割

                # print tmp_num
        lst_num = [int(tmp_num.strip('/').split('/')[0]),int(tmp_num.strip('/').split('/')[-1])]
        # lst_result.append(tmp_num)    # 原来的
        lst_result.append(tuple(lst_num))

    # print lst_result
    return lst_result