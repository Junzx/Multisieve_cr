# coding: utf-8
"""
调用LSTM得到的结果完成代词消解
"""
from __future__ import division
from MentionDetection.LSTM_labeled_data.load_lstm_labeled_data import load_lstm_data
import LoadConll
import config

dic_all_sent = load_lstm_data()

def count_md_prf(gold_data, result_data):
    """
    假设一共有10篇文章，里面4篇是你要找的。
    根据你某个算法，你认为其中有5篇是你要找的，但是实际上在这5篇里面，只有3篇是真正你要找的。
    那么你的这个算法的precision是3/5=60%，也就是，你找的这5篇，有3篇是真正对的
    这个算法的recall是3/4=75%，也就是，一共有用的这4篇里面，你找到了其中三篇。
    """

    set_right = set(gold_data)
    set_auto = set(result_data)

    precision = len(set_right.intersection(set_auto)) / len(set_auto)
    recall = len(set_right.intersection(set_auto)) / len(set_right)
    f_score = (precision * recall * 2) / (precision + recall)

    return (precision, recall, f_score)

def Mention_Detection(file_):
    obj_document = LoadConll.load_one_file_for_md(file_)

    lst_mention_idx = []

    sent_id = 0
    sent_lst_tokens = []
    # 以句子为单位创建sentence对象并提取表述
    for token in obj_document.lst_tokens:
        if token.sent_id == sent_id:
            sent_lst_tokens.append(token)

        if token.sent_id != sent_id:
            sentence_list_without_space = [t.word_itself.decode('utf-8') for t in sent_lst_tokens]
            token_id_lst = [t.token_id for t in sent_lst_tokens]
            sentence_without_space = ''.join(sentence_list_without_space)
            line_obj = dic_all_sent.get(sentence_without_space, 'No')

            if line_obj != 'No':  # 说明找到了记录
                pred_label =  line_obj.pred_label

                tmp = []
                for idx, label in enumerate(pred_label):
                    if label == u'B':   # 开头
                        tmp.append(idx)

                    elif label == u'I':
                        tmp.append(idx)
                    elif label == u'O' and tmp != []:   # 应该取出刚刚的
                        start_token_id = token_id_lst[tmp[0]]
                        end_token_id = token_id_lst[tmp[-1]]
                        lst_mention_idx.append((start_token_id, end_token_id))
                        del tmp[:]
            else:
                print '么有：'
                print sentence_without_space

            del sent_lst_tokens[:]
            sent_lst_tokens.append(token)
            sent_id += 1


    # 正确的标注数据
    gold_data = []
    gold_document = LoadConll.load_one_file(file_)  # 用于计算prf

    for mention in gold_document.lst_mentions:
        gold_data.append((mention.lst_tokens[0].token_id,
                        mention.lst_tokens[-1].token_id))


    return count_md_prf(gold_data, lst_mention_idx)

def __unit_test(vars='test'):
    if vars == 'train':
        folder_path = config.gold_train
    elif vars == 'test':
        folder_path = config.gold_test
    elif vars == 'error':
        folder_path = config.error_file_test

    test_files = config.get_var_files(folder_path)
    # test_file = 'test.v4_gold_conll'
    all_p = all_r = all_f = all_counter = 0.0
    for file_idx, file_ in enumerate(test_files):
        try:
            res = Mention_Detection(file_)
            print file_
            print 'File: %s of %s' % (file_idx, len(test_files))

            print res
            all_counter += 1
            all_p += res[0]
            all_r += res[1]
            all_f += res[2]
        except ZeroDivisionError:
            print '出错！', file_
            continue

    print '---------------', all_counter, '-------------'
    print all_p / all_counter
    print all_r / all_counter
    print all_f / all_counter
    print



if __name__ == '__main__':

    __unit_test()