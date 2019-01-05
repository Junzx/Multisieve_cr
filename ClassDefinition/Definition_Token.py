# -*- coding: UTF-8 -*-
from __future__ import division
from copy import deepcopy

class Token(object):
    """
    定义一个token结构
    """
    def __init__(self):
        self.sent_id = 0    # 所在的句子 的id
        self.word_id = 0    # 在句子中的id
        self.token_id = 0   # 该token的唯一uid
        self.word_itself = ''   # 中文
        self.pos_info = ''  # 该token的词性标注信息
        self.parse_info = ''   # 该token的句法树信息
        self.speaker = ''   # ！
        self.ner = '-' # 命名实体标签
        self.np_info = '-'  # coref id
        self.line = ''      # token那一行数据

    def set_attribute(self,tup_attr):
        """
        设置相关属性，接受一个tuple作为参数
        """
        self.sent_id = tup_attr[0]
        self.word_id = tup_attr[1]
        self.token_id = tup_attr[2]
        self.word_itself = tup_attr[3]#.encode('gbk')  # 转换为Unicode
        self.pos_info = tup_attr[4]
        self.parse_info = tup_attr[5]
        self.speaker = tup_attr[6]
        self.ner = tup_attr[7]
        self.np_info = tup_attr[8]
        self.line = tup_attr[-1]

    def get_class_attribute(self):
        return self.__dict__

if __name__ == '__main__':
    token = Token()