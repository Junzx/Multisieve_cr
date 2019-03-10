# coding:utf-8
"""读取cnn判断的动物属性识别结果"""

import cPickle
import config
from os import name


def _load_cPickle(file_):
    if name == 'posix':
        with open(file_, 'rb') as hdl:
            return cPickle.load(hdl)
    elif name == 'nt':
        with open(file_, 'r') as hdl:
            return cPickle.load(hdl)


def get_animacy_info_dict():
    if name == 'posix':
        animacy_info = _load_cPickle(config.project_path + '/Experiment/ExperimentResult/temp.dat')
    elif name == 'nt':
        animacy_info = _load_cPickle(config.project_path + '\Experiment\ExperimentResult\\temp.dat')
    animacy_info_dict = {}
    for item in animacy_info:
        animacy_info_dict.setdefault(item[0], item[1])
    return animacy_info_dict

if __name__ == '__main__':
    get_animacy_info_dict()