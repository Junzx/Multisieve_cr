# -*- coding: UTF-8 -*-
"""
作为main函数
"""
from LoadConll import load_one_file
from Multisieve.pronounce_cr import pronoun_sieve

def main(file_):
    document_object = load_one_file(file_)
    document_object = pronoun_sieve(document_object)
    print ''


if __name__ == '__main__':
    # test_file = 'small_test.conll'
    test_file = 'test.v4_gold_conll'
    main(test_file)