# coding: utf-8
"""
答辩期间找例子用
"""
import LoadConll
import api_cr_one_file
import config
import os
import api_md_one_file
from SubjectUtils.unit_test_utils import print_gold_cluster, print_cluster

choose_file1 = '/opt/tmp/DataSets/conll_test/test/vom_0289_000.v4_gold_conll'
choose_file2 = '/opt/tmp/DataSets/conll_test/test/cbs_0039_000.v4_gold_conll'
choose_file3 = '/opt/tmp/DataSets/conll_test/test/cnr_0119_000.v4_gold_conll'
choose_file4 = '/opt/tmp/DataSets/conll_test/test/cnr_0049_000.v4_gold_conll'
choose_file5 = '/opt/tmp/DataSets/conll_test/test/cnr_0029_000.v4_gold_conll' # 反例


def unit_test(file_):
    # document_object = load_one_file(file_)
    # res = LoadConll.load_one_file_for_md(file_)
    # api_md_one_file.main(res)
    # api_cr_one_file.main(res)
    res = api_cr_one_file.main(file_)
    print
    key_file = res.original_document_path
    res_file = config.result_folder + res.document_file_name + '.v4_result_conll'

    print key_file
    print res_file
    from Scorer.api_prf import get_one_file_prf
    print 'MUC:',get_one_file_prf(key_file, res_file, 'muc')
    print 'BCUB:', get_one_file_prf(key_file, res_file, 'bcub')
    os.remove(res_file)
    print_gold_cluster(res)
    print
    print
    print_cluster(res)

unit_test(choose_file1)
unit_test(choose_file2)
unit_test(choose_file3)
unit_test(choose_file4)
unit_test(choose_file5)
