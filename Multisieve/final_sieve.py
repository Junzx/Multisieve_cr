# coding: utf-8
"""
最后一轮，用于删除单独的表述
"""
from SubjectUtils.unit_test_utils import get_entities
from pprint import pprint
import SubjectUtils.sieve_utils as sieve_util
@sieve_util.sieve_timer
def filter_sieve(obj_document):
    entities = get_entities(obj_document, 'auto')

    # 找到待删除的独立表述
    # del_mention_id = [] # 待删除的表述的Mention id
    # for entity_id, entity in entities.items():
    #     if entity_id == -1:
    #         for m in entity:
    #             del_mention_id.append(m.mention_id)
    #     if len(entity) == 1:
    #         del_mention_id.append(entity[0].mention_id)

    # pprint(entities)
    # return obj_document
    if -1 in entities.keys():
        del_mention_id = [mention.mention_id for mention in entities[-1]]

        result = filter(lambda i: i.mention_id not in del_mention_id, obj_document.lst_mentions)
        obj_document.lst_mentions = result
    return obj_document