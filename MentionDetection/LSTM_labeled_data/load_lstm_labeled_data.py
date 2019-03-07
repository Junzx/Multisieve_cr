# coding: utf-8
"""
读取文件用
"""

class one_line(object):
    def __init__(self):
        self.line_idx = 0
        self.sentence_with_space = ''
        self.sentence_without_space = ''
        self.sentence_list = []
        self.true_label = []
        self.pred_label = []

def __load(file_):
    with open(file_, 'r') as hdl:
        return map(lambda str_: str_.strip('\r\n').strip('\n').decode('utf-8'),hdl.readlines())

def load_lstm_data():
    dic_all_data = {}

    sentence_file = 'test_source.txt'
    true_label_file = 'test_target.txt'
    pred_label_file = 'lstm_labeled_result.txt'

    sentence = __load(sentence_file)
    true_label = __load(true_label_file)
    pred_label = __load(pred_label_file)

    assert len(sentence) == len(true_label) == len(pred_label)
    line_length = len(sentence)

    for line_idx in range(line_length):
        line_sent = sentence[line_idx].split(' ')
        line_true_label = true_label[line_idx].split(' ')
        line_pred_label = pred_label[line_idx].split(' ')
        try:
            assert len(line_sent) == len(line_true_label) == len(line_pred_label)
        except AssertionError:
            print line_sent
            continue
        else:
            line_obj = one_line()
            line_obj.line_idx = line_idx
            line_obj.sentence_with_space = sentence[line_idx]
            line_obj.sentence_without_space = ''.join(line_sent)
            line_obj.sentence_list = line_sent
            line_obj.true_label = line_true_label
            line_obj.pred_label = line_pred_label
        # if line_obj.sentence_without_space not in dic_all_data:
        #     dic_all_data.setdefault(line_obj.sentence_without_space, [])
        # dic_all_data[line_obj.sentence_without_space].append(line_obj)
            dic_all_data.setdefault(line_obj.sentence_without_space, line_obj)

    return dic_all_data


if __name__ == '__main__':
    dic_all = load_lstm_data()
    print 'shit'
    for s, o in dic_all.items():
        print s
        print o.__dict__
        print '-------------------------'