# coding: utf-8

import config

files = config.get_var_files(config.result_folder, 'result')
print files
import LoadConll
f = files[10]
print f
data = LoadConll.load_one_file(f)
for m in data.lst_mentions:
    print m.chinese_word, m.mention_id, m.entity_id, m.start_token_id, m.end_token_id

print '=============='
import SubjectUtils.unit_test_utils

SubjectUtils.unit_test_utils.print_gold_cluster(data)