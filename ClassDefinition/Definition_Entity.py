# -*- coding: UTF-8 -*-

class Entity(object):
    def __init__(self):
        self.entity_id = 0     # 初始化为0
        self.attr_gender = 0    # 初始化为0
        self.attr_number = 0    # 初始化为0
        self.attr_animacy = 0   # 初始化为0
        self.lst_mentions = []  # 里面的元素是mention对象

    def set_entity_attribute(self):
        gender = 0
        number = 0
        animacy = 0
        # 考虑权重,进行投票
        for mention in self.lst_mentions:
            # 考虑性别
            gender += mention.weight * mention.gender
            # 考虑单复数
            number += mention.weight * mention.single
            # 考虑动物性
            animacy += mention.weight * mention.animacy

        # 遍历所有的表述,改变其属性
        for m in self.lst_mentions:
            if gender > 0:
                m.entity_attr_gender = 1
            elif gender < 0:
                m.entity_attr_gender = -1
            elif gender == 0:
                m.entity_attr_gender = 0

            if number > 0:
                m.entity_attr_number = 1
            elif number < 0:
                m.entity_attr_number = -1
            elif number == 0:
                m.entity_attr_number = 0

            if animacy > 0:
                m.entity_attr_animacy = 1
            elif animacy < 0:
                m.entity_attr_animacy = -1
            elif animacy == 0:
                m.entity_attr_animacy = 0
