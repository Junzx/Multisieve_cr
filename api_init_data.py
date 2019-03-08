# coding: utf-8
import config
import ConstantVariable
from time import clock,localtime,strftime
from ClassDefinition.Definition_Document import Document
from ClassDefinition.Definition_Token import Token

nlp_handle = ConstantVariable.nlp_handle

def normalize_article(var_string):
    var_string = var_string.replace('、','，')
    return var_string


def get_tokens(sentence):
    """
    分词，对self.sentence进行分词，返回一个编码为Unicode的list
    例子：[u'\u53f0\u94c1', u'\u6700\u8fd1', u'\u53ef\u4ee5',
    :return: list
    """
    return nlp_handle.word_tokenize(sentence)

def get_pos(sentence):
    """
    POS标注，返回一个list，内部元素是元组，分别是词语对应的POS tag
    例子：[(u'\u4e2a', u'M'), (u'\u5c0f\u65f6', u'NN'), (u'\u3002', u'PU')]
    :return:list(tuple)
    """
    return nlp_handle.pos_tag(sentence)

def get_ner(sentence):
    """
    进行NER标记，返回一个list，内部元素是元组，分别是词语对应的NER Label
    例子： [(u'\u4e2a', u'MISC'), (u'\u5c0f\u65f6', u'MISC'), (u'\u3002', u'O')]
    :return:list(tuple)
    """
    return nlp_handle.ner(sentence)

def get_parse(sentence):
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
    return nlp_handle.parse(sentence).split('\r\n')

# ================================================
# ================================================
# ================================================

class InitData(object):
    def __init__(self, article):
        self.article = article.strip('\n').strip()
        self.obj_document = Document()
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
            sentence = str_iter_sent  # 将一句话传入nlp tool中

            tokenize = get_tokens(sentence)
            ner = get_ner(sentence)
            pos_info = get_pos(sentence)
            parse_info = get_parse(sentence)

            print 'shit'
            assert len(tokenize) == len(ner) == len(pos_info) == len(parse_info)

            for idx in range(len(tokenize)):
                obj_token = Token()
                obj_token.sent_id = index_sent          # token所在的句子 的id
                obj_token.word_id = str(idx)    # token在句子中的id
                obj_token.token_id = word_id            # token唯一uid
                obj_token.word_itself = tokenize[idx]       # token中文
                obj_token.pos_info = pos_info[idx][1]
                obj_token.parse_info = parse_info[idx]
                obj_token.speaker = '-'
                obj_token.ner = ner[idx][1].strip('(').strip(')')
                obj_token.original_ner = ner[idx][1]
                obj_token.np_info = '-'
                obj_token.line = '    '.join(obj_token.__dict__.values().pop())

                self.obj_document.lst_tokens.append(obj_token)

                word_id += 1


            sent_id += 1


        return self.obj_document


def API(article):
    start = clock()
    article = normalize_article(article)
    obj_write2file = InitData(article)
    obj_document = obj_write2file.core_function()   # 写入文本
    end = clock()
    print '1.处理Article Finished! Use time:',(end - start),'s'
    return obj_document

if __name__ == '__main__':
    test_string = article = '台铁最近可以说是事故不断，昨天先是南下的‘自强号’列车撞上了一辆卡在铁轨当中的货柜车，而在傍晚又有一辆吊车在苗丽的后隆扯断了电车线，至于在晚上的８点半北上‘复兴号’又撞上了卡在铁轨当中的连接车，一天３起的铁路事故也造成台铁列车是严重误点，一直到今天凌晨的３：４５分才恢复正常通车。警铃持续示警，但是就是有人为了抢快抢过，害人害己，一辆满载木材的连接车晚间８点半抢越了台北板桥和树林之间的铁道，托板车底盘卡在铁轨上动弹不得，结果被‘复兴号’列车迎面撞击，现场一片混乱。连接车车窗破裂，火车车箱扭曲的停在夜色中，台铁立刻抢修，每个人都面色凝重，因为这是一天之内的第三起意外。祸不单行的是当晚在苗丽也是工程车辆出了状况。一辆吊车在通过苗丽后隆丰富火车站北侧平郊道时，吊钩扯断了电车线，造成供电停摆。三班列车当场在吊桥路段前进不得后退也不得。上千名旅客行程延误。面对这种情况，旅客不管是谁的错忍不住就开骂。让这三班列车动弹不得的元凶是这辆民间吊车，电车线被严重的扯坏了上百公尺，肇事的司机还一度绕跑逃走，最后总算被逮到。上午则是在苗丽市宜春路的平郊道发生了严重的车祸，一列‘自强号’列车刚刚开出苗丽车站，竟然发生两部大货车卡在平郊道上，‘自强号’来不及刹车就撞了上去，火车机车头严重受损，造成３人轻伤。由于现场电车线也遭到钩断，因此铁路交通在上午就整整停摆了３个小时。'
    API(test_string)