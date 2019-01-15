# -*- coding: UTF-8 -*-
from ClassDefinition.Definition_Mention import Mention

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
    entity_id = -1   # 表述对应的实体id，初始化

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
                obj_mention.gold_entity_id = str_coref_id
                obj_mention.lst_tokens = lst_tokens_in_np    # !注意，这里是浅拷贝，token的id是相同的
                obj_mention.set_other_attributes(obj_mention.lst_tokens)  # 调用此方法，设置其他的属性
                obj_mention.coref_id = str_coref_id

                # 在创建mention对象时候就设定一些属性
                # obj_mention.set_gender_single_animal()
                # print obj_mention.__dict__


                lst_all_mentions.append(obj_mention)

                mention_id += 1 # 更新
                # entity_id += 1  # 更新
    # self.lst_mentions = lst_all_mentions
    return lst_all_mentions # 其实是可以不返回的