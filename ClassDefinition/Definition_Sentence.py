# -*- coding: UTF-8 -*-
class Sentence(object):
    """
    对一个句子构建对象
    """
    def __init__(self):
        self.sent_id = 0
        self.lst_tokens = []    # 里面放的是token
        self.lst_mentions = []  # 放mention

    def get_token_by_id(self, token_id):
        for token in self.lst_tokens:
            if token.token_id == token_id:
                return token


    def get_sent(self):
        """
        获取这句话的文本
        """
        tmp = ''
        for token in self.lst_tokens:
            tmp += token.word_itself
        return tmp

    def get_sent_parse(self):
        """
        获取这句话的句法树信息
        :return:
        """
        parse = ''
        for token in self.lst_tokens:
            parse += token.parse_info.strip('\n')
        return parse

    def get_class_attribute(self):
        return self.__dict__

