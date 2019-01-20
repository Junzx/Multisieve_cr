# encoding: utf-8
from os import popen
from re import findall

def get_prf(gold_file, auto_file, method="muc"):
    """
    :param gold_file:
    :param auto_file:
    :param method: muc, bcub, ceafe, blanc
    :return: precision, recall, f1_score
    """
    order = 'perl scorer.pl {method} {gold_file} {auto_file}'.format(method = method,
                                                                      gold_file = gold_file,
                                                                      auto_file = auto_file)
    res = popen(order)
    for line in res:
        if line.startswith('Coreference') and \
                'Recall' in line and \
                'Precision' in line and \
                'F1' in line:
            tmp_res = line
            break
    else:
        return '', '', ''
    recall, precision, f1_score = findall('[\d]+%', tmp_res)
    return precision, recall, f1_score


if __name__ == '__main__':
    res_bcub = get_prf('test.v4_gold_conll', 'test.v4_res_conll', 'bcub')
    res_muc = get_prf('test.v4_gold_conll', 'test.v4_res_conll', 'muc')
    res_ceafe = get_prf('test.v4_gold_conll', 'test.v4_res_conll', 'ceafe')
    res_blanc = get_prf('test.v4_gold_conll', 'test.v4_res_conll', 'blanc')
    print 'Precision | recall | f1_score'
    print res_bcub
    print res_muc
    print res_ceafe
    print res_blanc
