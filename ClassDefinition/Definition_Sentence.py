# -*- coding: UTF-8 -*-
class Sentence(object):
    """
    对一个句子构建对象
    """
    def __init__(self):
        self.sent_id = 0
        self.lst_tokens = []    # 里面放的是token
        self.lst_mentions = []  # 放mention

    def get_class_attribute(self):
        return self.__dict__

