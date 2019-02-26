# encoding: utf-8
from os import popen, getcwd
from re import findall
import config

def get_prf(gold_file, auto_file, method="muc"):
    """
    :param gold_file:
    :param auto_file:
    :param method: muc, bcub, ceafe, blanc
    :return: precision, recall, f1_score
    """
    perl_path = config.project_path + '/Scorer/scorer.pl'
    order = 'perl {perl_path} {method} {gold_file} {auto_file}'.format(perl_path = perl_path,
                                                                        method = method,
                                                                        gold_file = gold_file,
                                                                        auto_file = auto_file)
    res = popen(order)
    # tmp = open('shit.txt','w')
    for line in res:
        # tmp.write(line + '\n')
        #
        if line.startswith('Coreference') and \
                'Recall' in line and \
                'Precision' in line and \
                'F1' in line:
            tmp_res = line
            # return tmp_res
            break
    else:
        return '', '', ''
    recall, precision, f1_score = findall("[\d.\d]+%", tmp_res)
    return precision, recall, f1_score


if __name__ == '__main__':
    from pprint import pprint
    key_file = 'merged_test.v4_gold_conll'
    res_file = 'merged_test.v4_result_conll'

    # 生成文件
    import merge_conll_file
    from os import remove, path
    try:
        remove(res_file)
        print '删除 旧 %s 成功！'% res_file
    except OSError:
        print '无旧文件  开始生成新文件'

    if not path.exists(key_file):
        merge_conll_file.api_('gold')
        print '生成 gold 文件成功！'

    merge_conll_file.api_('result')
    print '生成 新 %s 成功！' % res_file

    # 以下进行评价
    res_bcub = get_prf(key_file, res_file, 'bcub')
    res_muc = get_prf(key_file, res_file, 'muc')
    res_ceafe = get_prf(key_file, res_file, 'ceafe')
    res_blanc = get_prf(key_file, res_file, 'blanc')
    print '       Precision | recall | f1_score'
    print 'bcub:', res_bcub
    print 'muc:', res_muc
    print 'ceafe: ', res_ceafe
    print 'blanc: ', res_blanc

    dic = {
        'bcub': res_bcub,
        'muc': res_muc,
        'ceafe': res_ceafe,
        'blanc': res_blanc
    }
    print '-'* 30
    pprint(dic)
    # print get_prf('test.v4_gold_conll', 'test.v4_res_conll', 'all')