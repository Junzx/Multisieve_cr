# coding: utf-8

from ClassDefinition.Definition_Token import Token
from ClassDefinition.Definition_Entity import Entity
from ClassDefinition.Definition_Sentence import Sentence
from ClassDefinition.Definition_Mention import Mention
from ClassDefinition.Definition_Document import Document
from stanfordcorenlp import StanfordCoreNLP
import config
import ConstantVariable
import nlp_tools

nlp_path = config.nlp_path

nlp_handle = ConstantVariable.nlp_handle
nlp_tool = nlp_tools.NLP_tool(nlp_handle)
class InitDocument(object):
    """
    输入一段文本，然后返回一个document对象
    """
    def __init__(self, article):
        self.article = article

    def core_function(self):
        obj_document = Document()
        obj_document.first_line = 'Init Data has no first line!'
        lst_every_sentences = [str_sent + '。' for str_sent in self.article.strip('。').split('。')]

        token_id = 0
        for sent_idx, sentence in enumerate(lst_every_sentences):
            obj_sent = Sentence()
            obj_sent.sent_id = sent_idx
            tokenize = nlp_tool.get_tokens(sentence)    # 分词
            pos_info = nlp_tool.get_pos(sentence)
            ner = nlp_tool.get_ner(sentence)
            parse_done = nlp_tool.get_parse_done(sentence)

            print '------'
            assert len(tokenize) == len(pos_info) == len(ner) == len(parse_done)
            sentence_length = len(tokenize)
            
            for token_idx in range(sentence_length):
                token = Token()
                token.token_id = token_id
                token.sent_id = sent_idx # 句子id
                token.word_id = token_idx # 在句子中的位置
                token.pos_info = pos_info[token_idx][1]
                if ner[token_idx] == 'O':
                    token.ner = '*'
                else:
                    token.ner = ner[token_idx]
                token.word_itself = tokenize[token_idx]
                token.parse_info = parse_done[token_idx]
                token.line = '    '.join(map(lambda s:str(s),['SPACE', 0, token.word_id, token.word_itself, token.pos_info, token.parse_info, token.speaker, 'COREF']))

                #obj_sent.lst_tokens.append(token)
                obj_document.lst_tokens.append(token)
                token_id += 1
                print token.__dict__
            #obj_document.dic_sentence.set_default(obj_sent.sent_id, obj_sent)
        return obj_document


if __name__ == '__main__':
    article = '台铁最近可以说是事故不断，昨天先是南下的‘自强号’列车撞上了一辆卡在铁轨当中的货柜车，而在傍晚又有一辆吊车在苗丽的后隆扯断了电车线，至于在晚上的８点半北上‘复兴号’又撞上了卡在铁轨当中的连接车，一天３起的铁路事故也造成台铁列车是严重误点，一直到今天凌晨的３：４５分才恢复正常通车。警铃持续示警，但是就是有人为了抢快抢过，害人害己，一辆满载木材的连接车晚间８点半抢越了台北板桥和树林之间的铁道，托板车底盘卡在铁轨上动弹不得，结果被‘复兴号’列车迎面撞击，现场一片混乱。连接车车窗破裂，火车车箱扭曲的停在夜色中，台铁立刻抢修，每个人都面色凝重，因为这是一天之内的第三起意外。祸不单行的是当晚在苗丽也是工程车辆出了状况。一辆吊车在通过苗丽后隆丰富火车站北侧平郊道时，吊钩扯断了电车线，造成供电停摆。三班列车当场在吊桥路段前进不得后退也不得。上千名旅客行程延误。面对这种情况，旅客不管是谁的错忍不住就开骂。让这三班列车动弹不得的元凶是这辆民间吊车，电车线被严重的扯坏了上百公尺，肇事的司机还一度绕跑逃走，最后总算被逮到。上午则是在苗丽市宜春路的平郊道发生了严重的车祸，一列‘自强号’列车刚刚开出苗丽车站，竟然发生两部大货车卡在平郊道上，‘自强号’来不及刹车就撞了上去，火车机车头严重受损，造成３人轻伤。由于现场电车线也遭到钩断，因此铁路交通在上午就整整停摆了３个小时。'

    test = InitDocument(article)
    data = test.core_function()

    print '---------------------------'
    print data.first_line
    for token in data.lst_tokens:
        print token.line
