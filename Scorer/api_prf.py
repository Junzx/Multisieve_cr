# encoding: utf-8
from os import popen, getcwd,path, remove
import shutil
import hashlib
from re import findall
import config_sieve_order
import config
import time


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


def get_md5(file_path):
  md5 = -1
  if path.isfile(file_path):
    with open(file_path,'rb') as f:
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
  return md5


def get_one_file_prf(key_file, res_file, matrix='muc'):
    """
    用来评价一个conll文件的prf
    :param key_file: 类似于：/opt/tmp/DataSets/conll_test/test/chtb_0249_000.v4_gold_conll
    :param res_file: 类似于：/opt/tmp/DataSets/conll_test/test/chtb_0249_000.v4_result_conll
    """
    _, key_file_name = path.split(key_file)
    _, res_file_name = path.split(res_file)
    folder_path = config.project_path + '/Scorer/'
    func_key_file = folder_path + key_file_name # 待复制的路径
    func_res_file = folder_path + res_file_name

    shutil.copy(key_file, func_key_file)
    shutil.copy(res_file, func_res_file)

    res = get_prf(func_key_file, func_res_file, matrix)
    remove(func_key_file)
    remove(func_res_file)
    return res


# ==================================================
# ===================== 任 务 =======================
# ==================================================

def get_all_file_prf():

    import merge_conll_file
    from os import remove, path
    from pprint import pprint

    key_file = 'merged_test.v4_gold_conll'
    res_file = 'merged_test.v4_result_conll'
    _f_path = config.project_path + '/RunResults/Matrix_PRF.txt'

    def write_to_log(str_):
        prf_logger.write(str_ + '\n')
    prf_logger = open(_f_path, 'a+')

    # 写入sieve name
    write_to_log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for i in config_sieve_order.sieve_order:
        write_to_log("Sieve: %20s" % str(i.__name__))

    # 生成文件
    try:
        write_to_log("删除 旧 %s 文件，MD5：%s" % (key_file, get_md5(key_file)))
        remove(key_file)
    except OSError:
        pass
    try:
        write_to_log("删除 旧 %s 文件，MD5：%s" % (res_file, get_md5(res_file)))
        remove(res_file)
    except OSError:
        pass
    if not path.exists(key_file):
        merge_conll_file.api_('test')
        write_to_log("生成 新 %s 文件，MD5：%s" % (key_file, get_md5(key_file)))
    if not path.exists(res_file):
        merge_conll_file.api_('result')
        write_to_log("生成 新 %s 文件，MD5：%s" % (res_file, get_md5(res_file)))

    # 以下进行评价
    res_bcub = get_prf(key_file, res_file, 'bcub')
    res_muc = get_prf(key_file, res_file, 'muc')
    res_ceafe = get_prf(key_file, res_file, 'ceafe')
    res_blanc = get_prf(key_file, res_file, 'blanc')

    dic = {
        'bcub': res_bcub,
        'muc': res_muc,
        'ceafe': res_ceafe,
        'blanc': res_blanc
    }

    write_to_log('         Precision | recall | f1_score')
    write_to_log('-' * 40)
    for matrix, res in dic.items():
        write_to_log("%5s:    %s" % (matrix, '   '.join(['%6.2f' % float(i.replace('%', '')) for i in res])))
    write_to_log('\n\n')
    prf_logger.close()


if __name__ == '__main__':
    get_all_file_prf()