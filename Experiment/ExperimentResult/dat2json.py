# coding: utf-8
"""
dat 2 json
"""
import cPickle
import json

var = 'gender'

dat_file = "%s_result.dat"%var
json_file = "%s_result.json"%var

# load cPickle
with open(dat_file, 'rb') as hdl:
    obj = cPickle.load(hdl)

# save json
with open(json_file,'w') as write_hdl:
    json.dump(obj, write_hdl)