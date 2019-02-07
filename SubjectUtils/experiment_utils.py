# -*- coding: UTF-8 -*-
# import matplotlib.pyplot as plt
# from pylab import *
from os import remove, getcwd
from shutil import copyfile
import Scorer.api_prf
import numpy as np


def plot_result(res_dict):
    """
    画图
    """
    def __precent_2_float(str_):
        return float(str_.strip('%')) * 0.01

    sieve_order = res_dict.get('order_list')
    for score_name, scores in res_dict.items():
        if score_name == 'order_list':
            continue

        # 转换为array
        scores = np.array(scores)
        p_ = map(__precent_2_float, scores[:, 0])
        r_ = map(__precent_2_float, scores[:, 1])
        f_ = map(__precent_2_float, scores[:, 2])

        mpl.rcParams['font.sans-serif'] = ['SimHei']
        plt.figure(figsize=(20, 10))
        x = sieve_order

        plt.plot(x,p_,marker='o',label = u'Precision')
        plt.plot(x,r_,marker = '*', label = u'Recall')
        plt.plot(x,f_,marker = '^',label = u'F_score')
        plt.legend()    # 让图例生效

        plt.xlabel(u"Sieves") #X轴标签
        plt.ylabel(u"Values") #Y轴标签
        plt.title(u"Matrix of " + score_name + u" | PRF of Each Sieves")

        plt.savefig('./RunResults/' + score_name + '.png')
        plt.close()


def get_document_prf(obj_document):
    """
    传入一个document对象，获取当前情况下它的prf，返回一个字典
    """
    document_prf = {
        'muc': None,
        'blanc': None,
        'ceafe': None,
        'ceafm': None,
        'bcub': None,
    }
    # gold_file
    gold_file = obj_document.original_document_path
    # result file
    res_file = obj_document.result_document_path
    # 写入tmp文件
    obj_document.write_to_file(res_file)

    # 目的路径
    target_folder = getcwd() + '/Scorer/'
    gold_target_file = target_folder + obj_document.document_file_name + '.v4_gold_conll'

    result_target_file = target_folder + obj_document.document_file_name + '.v4_result_conll'

    # 复制文件
    copyfile(gold_file, gold_target_file)
    copyfile(res_file, result_target_file)

    # 调用perl
    res_muc = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "muc")
    res_blanc = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "blanc")
    res_ceafe = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "ceafe")
    res_ceafm = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "ceafm")
    res_bcub = Scorer.api_prf.get_prf(gold_target_file, result_target_file, "bcub")

    # 删除复制过去的文件
    remove(gold_target_file)
    remove(result_target_file)

    # 删除那啥
    remove(res_file)

    document_prf['muc'] = np.array(res_muc)
    document_prf['blanc'] = np.array(res_blanc)
    document_prf['ceafe'] = np.array(res_ceafe)
    document_prf['ceafm'] = np.array(res_ceafm)
    document_prf['bcub'] = np.array(res_bcub)

    return document_prf

