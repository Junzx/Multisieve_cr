# coding:utf-8
"""读取cnn判断的动物属性识别结果"""

import config
from os import name
import json
import logging

logger = logging.getLogger("Corpus_Loader")

def _load_json(file_):
    with open(file_, 'r') as hdl:
        return json.load(hdl)

def get_animacy_info_dict():
    logger.info("Load Animacy.json")
    if name == 'posix':
        animacy_info = _load_json(config.project_path + '/Experiment/ExperimentResult/animacy_result.json')
    elif name == 'nt':
        animacy_info = _load_json(config.project_path + '\Experiment\ExperimentResult\\animacy_result.json')
    animacy_info_dict = {}
    for item in animacy_info:
        animacy_info_dict.setdefault(item[0], item[1])
    return animacy_info_dict

def get_gender_info_dict():
    logger.info("Load Gender.json")
    if name == 'posix':
        gender_info = _load_json(config.project_path + '/Experiment/ExperimentResult/gender_result.json')
    elif name == 'nt':
        gender_info = _load_json(config.project_path + '\Experiment\ExperimentResult\\gender_result.json')
    gender_info_dict = {}
    for item in gender_info:
        gender_info_dict.setdefault(item[0], item[1])
    return gender_info_dict


if __name__ == '__main__':
    res = get_animacy_info_dict()
    print len(res)
    print res.items()[:10]