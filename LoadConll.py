# coding:utf-8
# import Data_Class
import ClassDefinition.Definition_Entity
import ClassDefinition.Definition_Mention
import ClassDefinition.Definition_Sentence
import ClassDefinition.Definition_Token
import ClassDefinition.Definition_Document

from ClassDefinition.Definition_Document import Document
from ClassDefinition.Definition_Sentence import Sentence
from ClassDefinition.Definition_Token import Token
from ClassDefinition.Definition_Mention import Mention
from ClassDefinition.Definition_Entity import Entity

import config
import logging


logger = logging.getLogger("load_data")

from pprint import pprint
# import Rebuild_Mention_Detection
# import Rebuild_Run_Data
from copy import deepcopy
EOF = '\r\n'


def string_to_tuple_tab(str_var):
    """
    接受一个字符串，去掉其中的所有空格并返回一个tuple变量
    """
    # return tuple([item for item in str_var.strip('\n').split(' ') if item != ''])
    return tuple(str_var.split('\t'))


def string_to_tuple_space(str_var):
    """
    接受一个字符串，去掉其中的所有空格并返回一个tuple变量
    """
    # return tuple([item for item in str_var.strip('\r\n').strip('\n').split(' ') if item != ''])
    return tuple([item for item in str_var.strip(EOF).split(' ') if item != ''])
    # return tuple(str_var.split('\t'))


def get_similarity_API(word1,word2):
    """
    返回两个词语的相似度
    """
    # return Rebuild_Run_Data.cilin_lib.similarity(word1,word2)
    return 1000

def load_one_file(str_iter_file_path):
    """
    输入一个conll文档，如果包含一个doc就返回那个doc object，否则返回一个list
    :param str_iter_file_path:
    :return:
    """
    logger.info("加载文档：%s"%str_iter_file_path)
    with open(str_iter_file_path, 'r') as hdl_file:  # 打开一个文件
        document_list = []
        flag_document = False  # 该flag表示这行数据是在document中的一条
        for str_line in hdl_file.readlines():  # 一行数据
            str_line = str_line.strip('\n')
            str_line = str_line.strip('\r\n')
            str_line = str_line.decode('utf-8')

            # document的开头
            if '#begin document' in str_line:
                flag_document = True
                obj_document = Document()  # 将document的数据放进去
                # obj_sent = Data_Class.Sentence()    # 创建sent对象
                token_id = 0  # token id从0开始计数
                sent_id = 0  # 句子编号，从0开始

                tmp_tuple = string_to_tuple_space(str_line)
                document_name = tmp_tuple[2].strip(';').strip('(').strip(')') + '_' + tmp_tuple[-1]
                obj_document.document_name = document_name
                obj_document.first_line = str_line
                obj_document.original_document_path = str_iter_file_path
                continue

            elif 'ＥＭＰＴＹ' in str_line:
                tup_token = string_to_tuple_space(str_line)
                # tup_token = string_to_tuple_tab(str_line)
                token_id += 1
                word_id = tup_token[2]  #
                word_itself = tup_token[3].decode('utf-8')
                pos_info = tup_token[4]  # 词性
                syntax_info = tup_token[5]  # 句法树

                tup_data = (
                    sent_id,  # 1
                    word_id,  # 2
                    token_id,  # 3
                    word_itself,  # 4
                    pos_info,  # 5
                    syntax_info,  # 6
                    '',  # 7
                    '-',  # 8
                    '-',  # 9
                    '    '.join(str_line.strip().split()[:-1])#.encode('utf-8') #9
                    # str_line.strip('\n')
                )
                # 创建token对象
                obj_token = Token()
                obj_token.set_attribute(tup_data)

                # 将token对象放在这个document的obj里
                obj_document.lst_tokens.append(obj_token)
                # obj_document.dic_tokens.setdefault(obj_token.token_id, obj_token)

            # 普通的一行数据
            elif flag_document and 'ＥＭＰＴＹ' not in str_line and '#end' not in str_line:

                tup_token = string_to_tuple_space(str_line)
                if tup_token == (): # 说明是空行
                    # print('shit空行', repr(str_line),len(str_line))
                    sent_id += 1  # tuple为空，sent id +1，说明这个是个空行，在数据中表示下一句话
                elif len(tup_token) > 1:
                    token_id += 1
                    word_id = tup_token[2]  #
                    word_itself = tup_token[3]
                    pos_info = tup_token[4]  # 词性
                    syntax_info = tup_token[5].strip('\r\n').strip('\n')  # 句法树
                    speaker = tup_token[9]  # speaker,有的文件没有
                    attribute = tup_token[10]
                    coref_info = tup_token[-1]  # 最后一列的信息

                    # 处理一下attribute标签
                    attribute = attribute.strip('(').strip(')')
                    if len(attribute) > 1:
                        attribute = attribute.strip('*')

                    tup_data = (
                        sent_id,  # 1
                        word_id,  # 2
                        token_id,  # 3
                        word_itself,  # 4
                        pos_info,  # 5
                        syntax_info,  # 6
                        speaker,  # 7
                        attribute,  # 8
                        coref_info,  # 9
                        '    '.join(str_line.strip().split()[:-1])#.encode('gbk') # 10
                        # str_line.strip('\n')
                    )

                    # 创建token对象
                    obj_token = Token()
                    obj_token.set_attribute(tup_data)
                    # print(obj_token.get_class_attribute())

                    # 将token对象放在这个document的obj里
                    obj_document.lst_tokens.append(obj_token)
                    # obj_document.dic_tokens.setdefault(obj_token.token_id, obj_token)

            elif '#end document' in str_line:
                flag_document = False
                # 注意这里,先获取普通的,然后拷贝给gold,gold中的mention entity id依靠其中的token 最后一列来控制
                # if obj_data.lst_tokens != []:
                    # obj_data.gold_mentions = extract_mention(obj_data.lst_tokens)
                    # obj_data.lst_mentions = extract_mention(obj_data.lst_tokens)
                    # print len(obj_data.lst_mentions)


                # 构建document的一些内容
                obj_document.api_set_some_attribute()
                document_list.append(obj_document)

                # obj_data.set_token_dict()
                # for id,t in obj_data.dic_tokens.items():
                #     print(id, t.get_class_attribute())


                # obj_data.gold_mentions = deepcopy(obj_data.lst_mentions)    # 如果进行MD，就注释这句话；如果进行CR，不注释
                # del obj_data.lst_mentions[:]    # !重要! 如果进行Mention Detection就不注释这句话

                # 对gold mentions创建entity id
                # for gold_mention in obj_data.gold_mentions:
                #     first_np_info = gold_mention.lst_tokens[0].np_info
                #     end_np_info = gold_mention.lst_tokens[-1].np_info
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
                #         elif '|' in gold_mention.lst_tokens[0].np_info:
                #             gold_mention.entity_id = first_np_info.split('|')[0].strip('(').strip(')')

                # 设置每个mention的权重
                # lst_keyword = [dic['word'] for dic in obj_data.lst_key_words]
                # for mention in obj_data.lst_mentions:
                #     weight = max([get_similarity_API(mention.chinese_word,keyword.decode('utf-8').encode('utf-8')) for keyword in lst_keyword])
                #     mention.weight = weight

                # obj_data.set_mention_dict()
                # obj_data.original_document_path = str_iter_file_path
                # obj_data.result_document_path = str_iter_file_path.replace('gold','result')

    logger.info("加载文档完毕！此文档共有%d个doc对象"%len(document_list))
    if len(document_list) == 1:
        return document_list[0]
    else:
        return document_list

def extract_mention(lst_tokens):
    """
    根据一个token list，根据最后一列信息，构建mention对象
    :param lst_token: 一列token 对象
    :return:[<__main__.NP object at 0x02B497F0>, <__main__.NP object at 0x02B49810>, ...] 返回的list中是np对象
    update:2018年2月28日
    这里的lst_token默认作为self.lst_token
    """
    # 初始化工作
    lst_all_mentions = []  # 放所有的NP对象的list

    stack = []
    lst_cols = [token.np_info for token in lst_tokens]  # 抽取最后一列的共指信息

    mention_id = 0  # 表述的唯一uid
    entity_id = 0   # 表述对应的实体id，初始化

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
                    lst_tokens_in_np.append(lst_tokens[i])  # np_tokens 里面放的是token的对象，比如1~3个token是一个np

                obj_mention = Mention()
                obj_mention.mention_id = mention_id
                obj_mention.entity_id = entity_id
                obj_mention.lst_tokens = lst_tokens_in_np    # !注意，这里是浅拷贝，token的id是相同的
                obj_mention.set_other_attributes()  # 调用此方法，设置其他的属性
                obj_mention.coref_id = str_coref_id

                # 在创建mention对象时候就设定一些属性
                # obj_mention.set_gender_single_animal()
                # print obj_mention.__dict__


                lst_all_mentions.append(obj_mention)

                mention_id += 1 # 更新
                entity_id += 1  # 更新
    # self.lst_mentions = lst_all_mentions
    return lst_all_mentions # 其实是可以不返回的

if __name__ == '__main__':
    from os import listdir
    # folder = config.path_test_folder
    # files = [folder + i for i in listdir(folder) if 'gold' in i]
    # test = load_one_file('test.v4_gold_conll')
    logger.info("开始执行")
    test = load_one_file('test.v4_gold_conll')
    logger.info("结束执行")
    # pprint(test.get_class_attribute())
    # from sys import getsizeof
    # print(getsizeof(test))
    # test.write_to_file()
    # for t in test.dic_tokens.values():
    #     print(t.line)