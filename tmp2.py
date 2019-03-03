# coding:utf-8
"""
读取test文件夹所有文件，提取出所有的候选表述
"""
import LoadConll
import config

files = config.get_var_files(config.gold_test)

candidate_mention = open('candidate_mentions.txt', 'w')

for file_ in files:
    tmp_mention = []
    data = LoadConll.load_one_file(file_)
    for mention in data.lst_mentions:
        tmp_mention.append(mention.chinese_word)

    for word in tmp_mention:
        candidate_mention.write(word + '\n')

    print 'write: ', file_, ' success!'

candidate_mention.close()
