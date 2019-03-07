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

class MentionDetectionUtils(object):
    """
    用于进行MentionDetection时的方法
    """
    def __init__(self):
        self.obj_document = 0

    def make_to_sentence(self, lst_tokens):
        """
        测试用，将句法信息合成为一句话
        返回类似于：        (TOP(IP(NP(NP0) (NP1)) (VP(ADVP2) (PP3 (NP(DP4) (NP5))) (VP6 7 (NP8))) 9))
        """
        str_sentence = ''
        del_sent = ''
        for token_id in lst_tokens:
            token = self.obj_document.get_token_by_id(token_id)
            syntax = deepcopy(token.syntax_info)
            # str_sentence += syntax.replace('*', obj_iter_token.word_id)         # 用word id替换*
            str_sentence += syntax.replace('*', str(token.token_id))    # test，用token id替换*
            str_sentence += ' '
        return str_sentence

    def exact_composition(self, str_sentence, composition):
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

    def exact_word(self, lst_var):
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


class MentionDetection(object):
    def __init__(self,obj_document):
        self.obj_document = obj_document

        self.utils = MentionDetectionUtils()
        self.utils.obj_document = self.obj_document # !注意，这里传递的是引用，不是deepcopy的形式

    def core_function(self):
        # print obj_document_init_data.get_class_attribute()
        index_sent_id = 0   # 句子的编号
        lst_sent_tokens = []    # 一个句子的token object

        # 放一个document的sent list，是list套list的形式, [ [token1,token2](句子1),[token0,token1,..,](句子2),...,]
        lst_all_sent_tokens = []
        for obj_iter_token in self.obj_document.lst_tokens:
            if obj_iter_token.sent_id == index_sent_id: # 句子计数器
                lst_sent_tokens.append(obj_iter_token.token_id) # 下面还有一处需同步修改

            elif obj_iter_token.sent_id == index_sent_id + 1:   # 如果当前的token属于下句话
                index_sent_id += 1  # index更新
                lst_tmp = deepcopy(lst_sent_tokens)
                lst_all_sent_tokens.append(lst_tmp)
                del lst_sent_tokens[:]  # 清空
                lst_sent_tokens.append(obj_iter_token.token_id) # 这里要跟上面同步修改

            if obj_iter_token == self.obj_document.lst_tokens[-1]:
                lst_tmp = deepcopy(lst_sent_tokens)
                lst_all_sent_tokens.append(lst_tmp)

        lst_all_num_composition = []    # 一个document中所有的NP的list，[[(0, 0), (1, 1), (5, 5)], [(8, 9), (9, 9)]]
        for lst_sent_token_id in lst_all_sent_tokens:   # 一次选取一个list，包含一句话的所有token id
            num_composition = self.__exact_word(lst_sent_token_id, 'NP') # 抽取NP
            lst_all_num_composition.append(deepcopy(num_composition))

        self.set_mention_info(lst_all_num_composition)  # 根据list，对构成mention的每个token的np info属性进行设置

        # 以下部分进行实际的表述提取工作
        # 1. 根据token list抽取表述
        lst_mention_heuristic = self.obj_document.extract_mention()
        self.obj_document.lst_mentions.extend(lst_mention_heuristic)

        # 2. 抽取所有的命名实体
        lst_mention_ner = self.obj_document.extract_named_entity()
        self.obj_document.lst_mentions.extend(lst_mention_ner)

        # TODO: 3. 将可能没有检测出的表述加入候选表述
        lst_mention_other = self.obj_document.extract_other_mentions()
        self.obj_document.lst_mentions.extend(lst_mention_other)


        # TODO: 3. 删除不可能是表述的mention，对lst_mentions进行处理操作
        self.obj_document.delete_some_mentions()

        # self.obj_document.lst_mentions = list(set(self.obj_document.lst_mentions))  # 去重
        self.obj_document.distinct_mentions()   # 先去重
        self.obj_document.set_sentence_mentions()
        self.obj_document.set_mention_dict()    # 这句在这个函数的最后一步调用，目的是构建那个dict（见DataClass line95）
        self.obj_document.set_abstracts()   # 调用这个函数，生成摘要等信息
        return self.obj_document


    def __exact_word(self, lst_tokens, composition):
        """
        给定一个list的token，抽取其中的元素，如“NP” | composition为待查找的成分
        """
        str_sentence = self.utils.make_to_sentence(lst_tokens) # 构成一句话
        composition = self.utils.exact_composition(str_sentence, composition)   # 抽取NP
        num_composition = self.utils.exact_word(composition)
        return num_composition  # [(0, 0), (1, 1), (5, 5)]

    def set_mention_info(self,lst_all_num_composition):
        """
        设置mention中的每个token的npinfo
        2018年2月28日
        """
        # 例如：lst_all_candidate_mention = [(0, 0), (1, 1), (5, 5), (8, 9), (9, 9)]
        lst_all_candidate_mention = [mention for lst_sent_mention in lst_all_num_composition for mention in lst_sent_mention]
        for index_mention,tup_candidate_mention in enumerate(lst_all_candidate_mention):
            int_first_token_id = tup_candidate_mention[0]
            int_second_token_id = tup_candidate_mention[1]

            if int_first_token_id == int_second_token_id:    # （9，9） 两个相等
                str_new_np_info = '(' + str(index_mention) + ')'
                self.__add_np_info(self.obj_document.get_token_by_id(int_first_token_id),str_new_np_info)

            elif int_first_token_id != int_second_token_id:  # （8，10）两个不等
                obj_start_token = self.obj_document.get_token_by_id(int_first_token_id)
                obj_end_token = self.obj_document.get_token_by_id(int_second_token_id)

                str_start_token_info = '(' + str(index_mention)
                str_end_token_info = str(index_mention) + ')'

                self.__add_np_info(obj_start_token,str_start_token_info)
                self.__add_np_info(obj_end_token,str_end_token_info)

    def __add_np_info(self, token, new_np_info):
        if token.np_info == '-':
            token.np_info = str(new_np_info)
        else:
            if '(' in token.np_info:
                token.np_info = token.np_info + '|' + new_np_info
            elif ')' in token.np_info:
                token.np_info = new_np_info + '|' + token.np_info

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

    # 根据token list构建sent对象
    sent_id = 0
    sent_lst_tokens = []
    # 以句子为单位创建sentence对象并提取表述
    for token in obj_document.lst_tokens:
        if token.sent_id == sent_id:
            sent_lst_tokens.append(token)

        if token.sent_id != sent_id:
            obj_sentence = init_sentence_object(lst_tokens=sent_lst_tokens)
            # obj_sentence = extract_mention_from_sentence(obj_sentence)
            dic_sentence.setdefault(sent_id, obj_sentence)
            sent_id += 1    # 更新sent id
            del sent_lst_tokens[:]
            sent_lst_tokens.append(token)

            for mention in obj_sentence.lst_mentions:
                obj_document.lst_mentions.append(mention)

    # 有的document可能就有一句话
    if sent_lst_tokens != []:
        obj_sentence = init_sentence_object(lst_tokens=sent_lst_tokens)
        # obj_sentence = extract_mention_from_sentence(obj_sentence)
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
    lst_mentions_from_ner = extract_named_entity(obj_sentence)

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

    for token in obj_sentence.lst_tokens:
        if token.ner != '-':
            flag_new_mention = True # 检测这个mention是不是已经在原list中存在
            for obj_iter_m in obj_sentence.lst_mentions:
                if (obj_iter_m.lst_tokens) == 1 and \
                    obj_iter_m.lst_tokens[0] == token:
                    flag_new_mention = False
                if flag_new_mention:
                    obj_mention = Mention()
                    obj_mention.mention_id = mention_id
                    # TODO：没写完

                    mention_id += 1
                    entity_id += 1
                    flag_new_mention = False

def old_extract_named_entity(obj_document):
    """
    提取命名实体
    """
    lst_all_mentions = []

    mention_id = len(obj_document.lst_mentions)
    entity_id = len(obj_document.lst_mentions)

    for token in obj_document.lst_tokens:
        if token.ner != '-':
            # 检测这个mention是不是已经在原list中存在
            flag_new_mention = True
            for obj_iter_mention in obj_document.lst_mentions:
                if len(obj_iter_mention.lst_tokens) > 1:
                    continue
                else:
                    if obj_iter_mention.lst_tokens[0] == token:
                        flag_new_mention = False
            if flag_new_mention:
                obj_mention = Mention()
                obj_mention.mention_id = mention_id
                obj_mention.entity_id = entity_id
                obj_mention.lst_tokens = [token]
                obj_mention.set_other_attributes(obj_document.lst_tokens)
                lst_all_mentions.append(obj_mention)

                mention_id += 1
                entity_id += 1
    return lst_all_mentions

def mention_filter(obj_sentence):
    pass



def __unit_test():
    from pprint import pprint
    data = load_one_file_for_md('test.v4_gold_conll')
    # res_data = Mention_Detection(data)
    data.lst_mentions = []
    name_eneity = extract_named_entity(data)

    for mention in res_data.lst_mentions:
        pprint(mention.__dict__)
        print '--------------------'
    print 'shit'

if __name__ == '__main__':
    __unit_test()
