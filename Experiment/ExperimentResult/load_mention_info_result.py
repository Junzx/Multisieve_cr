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
        animacy_info = _load_cPickle(config.project_path + '/Experiment/ExperimentResult/animacy_result.dat')
    elif name == 'nt':
        animacy_info = _load_cPickle(config.project_path + '\Experiment\ExperimentResult\\animacy_result.dat')
    animacy_info_dict = {}
    for item in animacy_info:
        animacy_info_dict.setdefault(item[0], item[1])
    return animacy_info_dict

def get_gender_info_dict():
    if name == 'posix':
        gender_info = _load_cPickle(config.project_path + '/Experiment/ExperimentResult/animacy_result.dat')
    elif name == 'nt':
        gender_info = _load_cPickle(config.project_path + '\Experiment\ExperimentResult\\animacy_result.dat')
    gender_info_dict = {}
    for item in gender_info:
        gender_info_dict.setdefault(item[0], item[1])
    return gender_info_dict


if __name__ == '__main__':
    get_animacy_info_dict()