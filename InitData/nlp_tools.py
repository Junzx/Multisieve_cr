# coding: utf-8

class NLP_tool(object):
    """
    这个类的方法用来切分数据
    如果需要使用先需要进行实例化
    """
    def __init__(self, nlp_handle):
        self.sentence = ''
        # self.nlp = StanfordCoreNLP(nlp_path, lang='zh')
        # self.nlp = beta_CoreCode.nlp  # 这里是全局的
        self.nlp = nlp_handle

    def get_tokens(self):
        """
        分词，对self.sentence进行分词，返回一个编码为Unicode的list
        例子：[u'\u53f0\u94c1', u'\u6700\u8fd1', u'\u53ef\u4ee5',
        :return: list
        """
        return self.nlp.word_tokenize(self.sentence)

    def get_pos(self):
        """
        POS标注，返回一个list，内部元素是元组，分别是词语对应的POS tag
        例子：[(u'\u4e2a', u'M'), (u'\u5c0f\u65f6', u'NN'), (u'\u3002', u'PU')]
        :return:list(tuple)
        """
        return self.nlp.pos_tag(self.sentence)

    def get_ner(self):
        """
        进行NER标记，返回一个list，内部元素是元组，分别是词语对应的NER Label
        例子： [(u'\u4e2a', u'MISC'), (u'\u5c0f\u65f6', u'MISC'), (u'\u3002', u'O')]
        :return:list(tuple)
        """
        return self.nlp.ner(self.sentence)

    def get_parse(self):
        """
        返回sentence的句法树，返回一个list
        例子：
        [u'(ROOT',
        u'        (ADVP (AD \u6574\u6574))',
        u'        (VP (VV \u505c\u6446) (AS \u4e86)',
        u'          (NP',
        u'            (QP (CD \uff13)',
        u'              (CLP (M \u4e2a)))',
        u'            (NP (NN \u5c0f\u65f6))))))',
        u'    (PU \u3002)))']
        :return:
        """
        return self.nlp.parse(self.sentence).split('\r\n')

    def get_deep_parse(self):
        """
        这个函数我也不知道是干嘛用的
        """
        return self.nlp.dependency_parse(self.sentence)

    def get_parse_done(self):
        for sent in self.sentence.strip('。').split('。'):
            sent = str(sent + '。')
            str_parse = self.nlp.parse(sent)
            # str_parse = self.nlp.parse(sent)
            str_parse = str_parse.replace('ROOT','TOP')
            lst_temp = []
            result = []
            # for hang in str_parse.split('\r\n'):
#             for hang in str_parse.split(beta_config.other_EOF):
            for hang in str_parse.split('\n'):
                lst_temp.append(hang)
                if r'\u' in repr(hang):   # 说明这行不同
                    result.append(''.join(copy(lst_temp)).encode('utf-8').strip())
                    del lst_temp[:]

            lst_parse = [replace_string(i) for i in result] # 在这一步调用函数，将词性等替换为*

            lst_return = []

            for s in lst_parse:
                temp = ''
                for i, c in enumerate(s):
                    temp += c
                    if i == len(s) - 1:
                        lst_return.append(temp)
                    elif c == '*':
                        if s[i+1] == '*':
                            lst_return.append(temp)
                            temp = ''

            return lst_return
