# -*- coding: UTF-8 –*-
"""
2018年2月27日重构
在本函数中，主要是对输入的文本进行处理，生成许多token对象和Document对象，并没有处理Mention对象
"""
from pprint import pprint
from time import clock,localtime,strftime
from os import name
# from Corpus.gender_classifier import gender_classifier
# from copy import copy,deepcopy
# import beta_config
import Utils
import Rebuild_Data_Class


if name == 'posix':
    separator = '/'
    EOF = '\r\n'
elif name == 'nt':
    separator = '\\'
    EOF = '\n'

class InitData(object):
    def __init__(self, article):
        self.article = article.strip(EOF).strip()
        self.nlp_tool = Utils.NLP_tool()
        self.obj_document = Rebuild_Data_Class.Document()
        self.obj_document.article = self.article

    def core_function(self):
        """
        2018年2月27日11点01分
        """
        lst_every_sentences = [str_sent + '。' for str_sent in self.article.strip('。').split('。')]
        word_id = 0
        sent_id = 0
        for index_sent,str_iter_sent in enumerate(lst_every_sentences):    # 用。分割，每次处理一句话
            # obj_sent = Sentence()   # 创建sent对象
            obj_sent = Rebuild_Data_Class.Sentence() # 新方法创建sent对象
            self.nlp_tool.sentence = str_iter_sent  # 将一句话传入nlp tool中

            for index_token,str_token in enumerate(self.nlp_tool.get_tokens()):
                obj_token = Rebuild_Data_Class.Token()
                obj_token.token_id = word_id            # token唯一uid
                obj_token.sent_id = index_sent          # token所在的句子 的id
                obj_token.word_id = str(index_token)    # token在句子中的id
                obj_token.word_itself = str_token       # token中文

                obj_sent.sent_id = sent_id
                obj_sent.lst_tokens.append(obj_token)   # 保存token对象
                word_id += 1

            for index_token,tup_pos in enumerate(self.nlp_tool.get_pos()):
                obj_sent.lst_tokens[index_token].pos_info = tup_pos[1]   # 该token的词性标注信息

            for index_token,str_parse in enumerate(self.nlp_tool.get_parse_done()):
                obj_sent.lst_tokens[index_token].syntax_info = str_parse  # 该token的句法树信息

            for index_token,tup_ner in enumerate(self.nlp_tool.get_ner()):
                if tup_ner[1] != 'O':
                    # obj_sent.lst_tokens[index_token].attribute = '(' + tup_ner[1] + ')'   # 命名实体标签
                    obj_sent.lst_tokens[index_token].attribute = tup_ner[1]   # 如果不加上左右括号

            self.obj_document.lst_sentences.append(obj_sent)    # 保存sent对象
            sent_id += 1

        # 对document 对象的lst_token进行处理
        for obj_sent in self.obj_document.lst_sentences:
            for obj_token in obj_sent.lst_tokens:
                self.obj_document.lst_tokens.append(obj_token)

        # self.obj_document.set_abstracts()   # 调用这个函数，生成摘要等信息
        self.obj_document.set_token_dict()  # 调用这个函数，构建{token_id:token}的字典
        return self.obj_document


def API(article):
    start = clock()
    article = Utils.normalize_article(article)
    obj_write2file = InitData(article)
    obj_document = obj_write2file.core_function()   # 写入文本
    end = clock()
    print '1.处理Article Finished! Use time:',(end - start),'s'
    return obj_document

if __name__ == '__main__':
    start = clock()
    article = '台铁最近可以说是事故不断，昨天先是南下的‘自强号’列车撞上了一辆卡在铁轨当中的货柜车，而在傍晚又有一辆吊车在苗丽的后隆扯断了电车线，至于在晚上的８点半北上‘复兴号’又撞上了卡在铁轨当中的连接车，一天３起的铁路事故也造成台铁列车是严重误点，一直到今天凌晨的３：４５分才恢复正常通车。警铃持续示警，但是就是有人为了抢快抢过，害人害己，一辆满载木材的连接车晚间８点半抢越了台北板桥和树林之间的铁道，托板车底盘卡在铁轨上动弹不得，结果被‘复兴号’列车迎面撞击，现场一片混乱。连接车车窗破裂，火车车箱扭曲的停在夜色中，台铁立刻抢修，每个人都面色凝重，因为这是一天之内的第三起意外。祸不单行的是当晚在苗丽也是工程车辆出了状况。一辆吊车在通过苗丽后隆丰富火车站北侧平郊道时，吊钩扯断了电车线，造成供电停摆。三班列车当场在吊桥路段前进不得后退也不得。上千名旅客行程延误。面对这种情况，旅客不管是谁的错忍不住就开骂。让这三班列车动弹不得的元凶是这辆民间吊车，电车线被严重的扯坏了上百公尺，肇事的司机还一度绕跑逃走，最后总算被逮到。上午则是在苗丽市宜春路的平郊道发生了严重的车祸，一列‘自强号’列车刚刚开出苗丽车站，竟然发生两部大货车卡在平郊道上，‘自强号’来不及刹车就撞了上去，火车机车头严重受损，造成３人轻伤。由于现场电车线也遭到钩断，因此铁路交通在上午就整整停摆了３个小时。'
    # article = '台铁最近可以说是事故不断。多人被困。'
    # article = '研究生院召开国际联合培养研究生归国汇报会暨项目宣讲会。来自数学科学学院，生命科学学院，资环学院，历史学院，政法学院，教育学院的十名研究生分享了他们参加研究生国际联合培养项目的心得体会，并就如何申请海外高校和科研机构，如何准备校内申请流程和签证流程，以及如何应对跨文化情境下的学术挑战为大家进行了详尽的解读。研究生院培养办公室范兴云，赵汀，刘旭介绍了研究生院国际联合培养的四大途径以及申请条件和申请方式。'

    # out_file = 'out_file.txt'
    obj_doc = API(article)
    # pprint(obj_doc.get_class_attribute())

    for token in obj_doc.lst_tokens:
        print token.word_itself,token.__dict__

    # for sent in obj_doc.lst_sentences:
    #     print sent.get_class_attribute()



    print '用时：',clock() - start,'s'