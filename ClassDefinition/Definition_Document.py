# -*- coding: UTF-8 -*-
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from copy import deepcopy

from ClassDefinition.Definition_Sentence import Sentence
from ClassDefinition.Definition_Entity import Entity
# from load_conll import load_one_file
import Definition_Mention
# import Definition_Entity
import config
from MentionDetection.exact_np_by_tree import extract_mention

import logging
logger = logging.getLogger("设置共指：")

EOF = '\n'

class Document(object):
    """
    给定一个file path的文件，读取文件
    """
    def __init__(self):
        self.document_name = ''
        self.lst_tokens = []    # 保存所有token object
        self.first_line = ''    # 第一句话

        # self.lst_mentions = []  # 保存所有mention object
        # self.lst_entities = []  # 放entity对象

        # ------ 以下参数只有在读取文件的时候才有用 -------
        # self.gold_mentions = [] # 正确的mention，只有当读取文件的时候才用这个属性 | 下标就是mention id
        # self.dic_gold_mentions = {}
        self.original_document_path = ''    # 文件的路径
        # self.log_cr_document_path = ''  # CR中的log路径
        # self.log_md_document_path = ''  # MD中的log路径


    def get_class_attribute(self):
        return self.__dict__

    def get_mention_by_id(self, mention_id):
        return self.lst_mentions[mention_id]

    def get_token_by_id(self, token_id):
        return self.dic_tokens.get(token_id)

    def get_some_tokens(self, lst_tokens_id):
        return [self.dic_tokens.get(token_id) for token_id in lst_tokens_id]


    # -----------------------------以上是定义的一些方法 ----------------------------------

    def api_set_some_attribute(self):
        self.document_file_name = self.document_name.split('/')[-1]
        self.result_document_path = self.original_document_path.replace('gold','result')
        self.__set_dict_attribute()
        self.__set_abstracts()
        self.__set_sentences()
        # logger.info("加载数据完成")
        self.dic_entity = {}   # cluster_id : cluster_object


    def __set_dict_attribute(self):
        """
        根据token list生成dict
        :return:
        """
        # 构建token dict
        self.dic_tokens = {}    # token_id : token object
        for token in self.lst_tokens:
            self.dic_tokens.setdefault(token.token_id, token)

        # 构建mention list
        self.lst_mentions = extract_mention(self.lst_tokens)

        # 构建mention dict
        self.dic_mentions = {}
        for mention in self.lst_mentions:
            self.dic_mentions.setdefault(mention.mention_id, mention)

        # 保存一份正确的结果作为最后的测试处理
        self.gold_mention = deepcopy(self.lst_mentions)

    def __set_abstracts(self):
        """
        设置关键字、摘要等
        """
        # 通过token list获取article
        self.article = ''   # document文本
        self.lst_abstract = []  # 放两句摘要 | item.index, item.weight, item.sentence
        self.lst_key_words = [] # 关键字list | item.word, item.weight
        # self.key_word = ''  # 关键词短语

        # 文本内容
        for token in self.lst_tokens:
            self.article += token.word_itself

        # 关键字
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=self.article, lower=True, window=2)
        self.lst_key_words = deepcopy(tr4w.get_keywords(20, word_min_len=1))

        # 关键短语
        # lst_tmp_phrases = tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2)
        # if len(lst_tmp_phrases) == 0:
        #     self.key_word = 'No-phrases'
        # else:
        #     self.key_word = lst_tmp_phrases[0]

        # 摘要
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=self.article, lower=True, source = 'all_filters')
        self.lst_abstract = deepcopy(tr4s.get_key_sentences(num=2))

        # 对每个mention计算权重
        lst_key_word = [item['word'] for item in self.lst_key_words]
        for mention in self.lst_mentions:
            if mention.chinese_word in lst_key_word:    # 说明这个是关键字
                mention.weight = [item['weight'] for item in self.lst_key_words if item['word'] == mention.chinese_word][0]

    def __set_sentences(self):
        """
        根据token dict 和mention list设定sentence
        必须在设定好token 和 mention后调用，否则报错
        """
        # self.lst_sentences = []
        self.dic_sentences = {} # 放sent对象

        max_sent_id = self.lst_tokens[-1].sent_id # 最后一个token的sent id
        # 先创建sent对象
        for sent_id in range(max_sent_id + 1):
            sent = Sentence()
            sent.sent_id = sent_id
            self.dic_sentences.setdefault(sent_id, sent)

        for token in self.lst_tokens:
            self.dic_sentences.get(token.sent_id).lst_tokens.append(token)

        for mention in self.lst_mentions:
            sent_id = mention.sent_id
            self.dic_sentences.get(sent_id).lst_mentions.append(mention)

    def __set_gold_mentions_old(self):
        """
        update：弃用——1.5
        根据一个token list，根据最后一列信息，构建mention对象
        :return:[<__main__.NP object at 0x02B497F0>, <__main__.NP object at 0x02B49810>, ...] 返回的list中是np对象
        """
        stack = []
        lst_cols = [token.np_info for token in self.dic_tokens.values()]  # 抽取最后一列的共指信息

        mention_id = 0  # 表述的唯一uid
        # entity_id = 0   # 表述对应的实体id，初始化

        for int_index_content, str_iter_content in enumerate(lst_cols):
            for int_index_each_char, str_each_char in enumerate(str_iter_content):  # str_each_char是每个信息的每个字符
                if str_each_char == '(':
                    stack.append(int_index_content)  # 压栈操作，将当前的index记录在栈中，表示这个左括号在总list中第几个位置

                    # sent_id = lst_token[int_index_content].sent_id  # 这个属于第几个sent
                elif str_each_char == ')':
                    int_index_match = stack.pop()  # 出栈操作，pop出右括号在当前list中第几个位置
                    lst_tmp_digits = []  # 用来存放数字的list
                    int_index_num = int_index_each_char - 1  # int_index_num 是紧邻右括号的左边的第一个字符的下标
                    while int_index_num >= 0:
                        str_j = str_iter_content[int_index_num]  # 根据下标取出右括号左边第一个字符
                        if str_j in '0123456789':  # 如果这个字符是数字的话
                            lst_tmp_digits.append(str_j)  # 将它添加到放数字的list中
                            int_index_num -= 1  # 下标向左移 判断下一个字符
                        else:  # 直到遇到不是数字的字符就break
                            break  # 这时候，int_index_content 就是 匹配右括号的那个位置
                    lst_tmp_digits.reverse()  # 将放数字的list倒过来（倒过来才是正确的顺序）

                    str_coref_id = ''.join(lst_tmp_digits)  # 拼出数字
                    lst_tokens_in_np = []
                    for i in range(int_index_match, int_index_content + 1):  # 根据索引确认
                        # lst_tokens_in_np.append(self.lst_tokens[i])  # np_tokens 里面放的是token的对象，比如1~3个token是一个np
                        lst_tokens_in_np.append(i + 1)  # np_tokens 里面放的是token的token_id

                    obj_mention = Definition_Mention.Mention()
                    obj_mention.mention_id = mention_id
                    obj_mention.entity_id = mention_id
                    obj_mention.gold_entity_id = str_coref_id
                    obj_mention.lst_tokens = lst_tokens_in_np    # !注意，这里是浅拷贝，token的id是相同的 update: token id
                    obj_mention.set_other_attributes([self.dic_tokens.get(token_id) for token_id in lst_tokens_in_np])  # 调用此方法，设置其他的属性
                    self.lst_mentions.append(obj_mention)
                    mention_id += 1 # 更新
                    # entity_id += 1  # 更新

        # for gold_mention in self.lst_mentions:
        #     first_token = self.dic_tokens.get(gold_mention.lst_tokens[0])
        #     end_token = self.dic_tokens.get(gold_mention.lst_tokens[-1])
        #     first_np_info = first_token.np_info
        #     end_np_info = end_token.np_info
        #
        #     if len(gold_mention.lst_tokens) == 1:
        #         if '|' not in first_np_info:
        #             gold_mention.entity_id = first_np_info.strip('(').strip(')')
        #         elif '|' in first_np_info:
        #             gold_mention.entity_id = first_np_info.split('|')[-1].strip('(').strip(')')
        #
        #     elif len(gold_mention.lst_tokens) > 1:
        #         if '|' not in first_np_info:   # 如果没有|
        #             gold_mention.entity_id = end_np_info.strip(')')
        #         elif '|' in first_np_info:
        #             gold_mention.entity_id = first_np_info.split('|')[0].strip('(').strip(')')
            # self.dic_gold_mentions.setdefault(gold_mention.mention_id, gold_mention)


    def get_candidate_mentions(self, obj_mention):
        """
        给定mention id并返回候选表述
        1. 获取mention的句子id
        2. 获取前n=3个sent对象（包括当前表述所在的句子）
        3. 从后向前选择sent对象，其中表述按照从左向右选取
        """
        sentence_distance = 2   # 表示 表述所在的句子，以及之前的 n 个句子
        sent_id = obj_mention.sent_id
        if sent_id <= sentence_distance :
            sent_id_list = reversed(range(0, sent_id + 1))
        else:
            sent_id_list = reversed(range(sent_id - sentence_distance, sent_id + 1))
        candidate_sentences = [self.dic_sentences[sentence_id] for sentence_id in sent_id_list]
        candidate_mentions = []
        tmp = 0
        for sentence in candidate_sentences:
            if sentence.sent_id == sent_id:
                tmp_candidate_mentions = [self.lst_mentions[mention_id]
                                          for mention_id in sentence.lst_mentions
                                          if mention_id < obj_mention.mention_id]
                candidate_mentions.extend(tmp_candidate_mentions)
                tmp += len(tmp_candidate_mentions)
            # todo：前面的sentence
            else:
                tmp_candidate_mentions = [self.lst_mentions[mention_id] for mention_id in sentence.lst_mentions]
                candidate_mentions.extend(tmp_candidate_mentions)
                tmp += len(tmp_candidate_mentions)
        return candidate_mentions

    def set_coref(self, mention_1, mention_2):
        """
        2018-5-4 重写的函数,写好后替代上面的函数.
        调用方法:self.obj_document.set_coref(candidate_mention.mention_id,mention.mention_id)
        """
        # mention_1 = self.lst_mentions[mention_id_1]
        # mention_2 = self.lst_mentions[mention_id_2]
        logger.info(" %s(id:%s) , %s(id:%s)"%(mention_1.chinese_word,str(mention_1.mention_id), \
                                                    mention_2.chinese_word, str(mention_2.mention_id)))
        mention_1_entity_id = str(mention_1.entity_id)
        mention_2_entity_id = str(mention_2.entity_id)

        # 1. 两个mention不以'E_'开头 → 没有任何一个表述的entity_id在dic_entity中
        if not mention_1_entity_id.startswith('E_') and not mention_2_entity_id.startswith('E_'):
            # i) 取j的mention_id,并将两个表述的entity_id设置相同

            # update： 如果是-1 那么就先设置为mention id
            if mention_2_entity_id == '-1':
                mention_2_entity_id = mention_2.mention_id

            entity_id = 'E_' + str(mention_2_entity_id)
            mention_1.entity_id = entity_id
            mention_2.entity_id = entity_id
            # ii) 创建cluster object
            obj_entity = Entity()
            # iii) 设置obj_cluster的相关属性
            obj_entity.entity_id = entity_id
            obj_entity.lst_mentions.append(mention_1)
            obj_entity.lst_mentions.append(mention_2)
            # iv) 设置属性变量
            obj_entity.set_entity_attribute()
            # v) 保存这个entity object
            self.dic_entity.setdefault(entity_id, obj_entity)
            # print mention_1.entity_id,mention_2.entity_id,' / ',mention_1,mention_2,' / ',entity_id#,obj_entity.lst_mentions


        # 2. 第二个mention以E_开头,这种情况通常是出现在上一个if结束后,第二个mention的entity id已经变成了E_开头
        elif not mention_1_entity_id.startswith('E_') and mention_2_entity_id.startswith('E_'):
            # i) 赋值
            entity_id = mention_2.entity_id
            mention_1.entity_id = entity_id
            # ii) 取出entity object
            obj_entity = self.dic_entity[entity_id]
            # iii) 将新的mention增加到list中
            obj_entity.lst_mentions.append(mention_1)   # mention_2已经在list中了
            # iv) 更新entity的属性
            obj_entity.set_entity_attribute()
            # v) 遍历所有的mention,统一entity id
            for mention in self.lst_mentions:
                if mention.entity_id == mention_1.entity_id and str(mention.entity_id) != '-1':
                    mention.entity_id = entity_id

        # 3. 第一个表述以E_开头,第二个不是,这里可能需要更新所有的表述的entity id
        elif mention_1_entity_id.startswith('E_') and not mention_2_entity_id.startswith('E_'):
            # i) 赋值
            entity_id = mention_1.entity_id
            mention_2.entity_id = entity_id
            # ii) 取出entity object
            obj_entity = self.dic_entity[entity_id]
            # iii) 将后面的mention加入list中
            obj_entity.lst_mentions.append(mention_2)
            # iv) 更新entity属性
            obj_entity.set_entity_attribute()
            # v)
            for mention in self.lst_mentions:
                if str(mention.entity_id) == mention_2_entity_id and str(mention.entity_id) != '-1':
                    mention.entity_id = entity_id

        # 4. 均以'E_'开头,但是两个表述都是相同的EntityID,这时候仅仅需要更新Entity object即可
        elif mention_1_entity_id.startswith('E_') and mention_2_entity_id.startswith('E_') and mention_1_entity_id == mention_2_entity_id:
            # i) 取出entity object
            # obj_entity = self.dic_entity[mention_1_entity_id]
            # ii) 新增
            pass

        # 5. 均以'E_'开头 | 这将导致两个cluster合并,约束取mention时不取E_开头的mention即可
        elif mention_1_entity_id.startswith('E_') and mention_2_entity_id.startswith('E_') and mention_1_entity_id != mention_2_entity_id:
            # i) 遍历
            for mention in self.lst_mentions:
                if str(mention.entity_id) == mention_1_entity_id:
                    mention.entity_id = mention_2_entity_id
            # ii) 取出entity object
            obj_entity = self.dic_entity[mention_2_entity_id]
            # iii) 取出要被合并的entity object中的mention list
            lst_del_mentions = self.dic_entity[mention_1_entity_id].lst_mentions
            # iv)
            for mention in lst_del_mentions:
                mention.entity_id = mention_2_entity_id
            # iv) 合并
            obj_entity.lst_mentions.extend(lst_del_mentions)
            # v) 删除要被合并的entity object
            del self.dic_entity[mention_1_entity_id]

        # ---
        # print 'set coref: ',
        # print mention_1.chinese_word, mention_2.chinese_word, ' | ',
        # print mention_1.mention_id, mention_2.mention_id, ' | ',
        # print mention_1.entity_id, mention_2.entity_id

    # ----------------------------- 定义写入文件的方法 -----------------------------------

    def write_to_log(self,sieve_name):
        """
        写入log文件
        """
        self.log_cr_document_path = config.path_log_folder + config.separator + 'log_CR_' + self.original_document_path.split(config.separator)[-1].split('.')[0] + '.txt'
        # self.__write_gold_data()    # 写入正确的结果

        dic_mentions = {}
        for mention in self.lst_mentions:
            if mention.entity_id not in dic_mentions:
                dic_mentions.setdefault(mention.entity_id,[])
            dic_mentions[mention.entity_id].append(mention)

        lst_single = []
        lst_plural = []
        for id in dic_mentions:
            if len(dic_mentions[id]) == 1:
                lst_single.append(dic_mentions[id])
            else:
                lst_plural.append(dic_mentions[id])

        with open(self.log_cr_document_path, 'a+') as hdl:
            hdl.write('-------------- ' + sieve_name + '--------------' + EOF)
            hdl.write('已聚类：' + config.conll_EOF)
            if len(lst_plural) == 0:
                hdl.write('None' + config.conll_EOF)
            for lst_mention in lst_plural:
                hdl.write(str(lst_mention[0].entity_id) + ':')
                for m in lst_mention:
                    hdl.write(m.chinese_word + ',' + str(m.mention_id) + ' | ')
                hdl.write(config.conll_EOF)
            hdl.write(config.conll_EOF)
            hdl.write('未聚类：' + config.conll_EOF)
            if len(lst_single) == 0:
                hdl.write('None' + config.conll_EOF)
            for lst_mention in lst_single:
                m = lst_mention[0]
                hdl.write(m.chinese_word + ',' + \
                          str(m.entity_id) + ',' + \
                          str(m.mention_id) + ' | ')
            hdl.write(EOF)

    def write_to_file(self,file_path = 'demo.txt'):
        """
        CR将调用这个函数来写入文件
        """
        self.update_entity_id() # 去掉E_ 开头
        for token in self.dic_tokens.values():
            token.np_info = '-'

        for mention in self.lst_mentions:
            if mention.entity_id == '-1':
                continue
            # for index_token,token in enumerate(mention.lst_tokens):
            len_tokens = len(mention.lst_tokens)
            entity_id = mention.entity_id

            if len_tokens == 1:
                # token.np_info = '(' + str(entity_id) + ')'
                self.adding_np_info(self.dic_tokens.get(mention.lst_tokens[0].token_id),'(' + str(entity_id) + ')')
            else:
                first_token_string = '(' + str(entity_id)
                # if mention.lst_tokens[0].np_info == '-':
                self.adding_np_info(self.dic_tokens.get(mention.lst_tokens[0].token_id),first_token_string)
                # elif mention.lst_tokens[0].np_info == first_token_string:
                    # first_token_string = first_token_string *2
                    # self.adding_np_info(mention.lst_tokens[0],first_token_string)

                second_token_string = str(entity_id) + ')'
                self.adding_np_info(self.dic_tokens.get(mention.lst_tokens[-1].token_id),second_token_string)

        with open(file_path,'a') as hdl:
            hdl.write(self.first_line)
            hdl.write(EOF)
            sent_id = 0
            for token in self.dic_tokens.values():

                if token.sent_id == sent_id + 1:
                    hdl.write(config.conll_EOF)
                    sent_id += 1
                hdl.write(token.line + ' ' + token.np_info + config.conll_EOF)
            hdl.write(config.conll_EOF + '#end document')

    def update_entity_id(self):
        """
        这个函数一般最后调用,用于对Mention去除E_
        """
        for mention in self.lst_mentions:
            mention.entity_id = str(mention.entity_id).strip('E_')

    def adding_np_info(self, token, new_string):
        # print token.word_itself,token.np_info,new_string,
        if token.np_info == '-':
            token.np_info = new_string
        # elif token.np_info != new_string:
        elif token.np_info != '-':
            # token.np_info = token.np_info + '|' + new_string
            token.np_info = new_string + '|' + token.np_info

    # ----------------------------- 定义一些输出用的方法 -----------------------------------
    def __mention_2_entity(self, var):
        """
        遍历所有的mention，构建entity
        """
        dic = {}
        for mention in self.lst_mentions:
            if var == 'auto':
                entity_id = mention.entity_id
            elif var == 'gold':
                entity_id = mention.gold_entity_id

            if entity_id not in dic:
                dic.setdefault(entity_id, [])
            dic[entity_id].append(mention)
        return dic

    def print_gold_cluster(self):
        """
        输出这个document的标准答案
        """
        print('标准答案（from file）：')
        dic = self.__mention_2_entity(var='gold')
        for entity_id, mention_list in dic.items():
            if len(mention_list) > 1:
                print('Entity_id:(',entity_id, ') ', )
                for m in mention_list:
                    print(m.chinese_word,',', m.mention_id, '| ',)
            print()

    def print_cluster(self):
        """
        输出 cluster数量大于1的entity
        """
        print('当前聚类情况（len(cluster)>1）：')
        dic = self.__mention_2_entity(var='auto')
        for entity_id, mention_list in dic.items():
            if len(mention_list) > 1:
                print('Entity_id:(',entity_id, ') ',)
                for m in mention_list:
                    print(m.chinese_word,',', m.mention_id, '| ',)
                print()

