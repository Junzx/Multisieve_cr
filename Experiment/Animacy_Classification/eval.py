# coding:utf-8
import tensorflow as tf
import numpy as np

import time
import os
import datetime
import data_helper
import parameters
from CNN_Network import CNN
from tensorflow.contrib import learn
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
FLAGS = parameters.FLAGS


FLAGS._parse_flags()    # TODO
# 输出FLAGS的属性
for attr, value in sorted(FLAGS.__flags.items()):
    print attr.upper(), value
print '-=-=-=-=-=-=' * 3

tuple_datas = (FLAGS.human_test_data, FLAGS.non_human_test_data)
FLAGS.eval_train = True # TODO:what is this?

if FLAGS.eval_train:
    x_raw, y_test = data_helper.load_data_and_labels(tuple_datas)
    y_test = np.argmax(y_test, axis = 1) # TODO:argmax ?

vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
x_test = np.array(list(vocab_processor.transform(x_raw)))

for i in range(10):
    print x_raw[i], y_test[i]
for i in range(-10,-1):
    print x_raw[i], y_test[i]
print '-=-=-=-=-=' * 3

checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
print dir(checkpoint_file)
print '-=' * 15

graph = tf.Graph()
with graph.as_default():
    sess = tf.Session()
    with sess.as_default():
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)

        # 通过name从graph中获取placeholder
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # 待处理的
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]
        batches = data_helper.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

        # 预测结果
        all_predictions = []
        for x_test_batch in batches:
            batch_predictions = sess.run(predictions, feed_dict = {input_x: x_test_batch, dropout_keep_prob: 1.0})
            all_predictions = np.concatenate([all_predictions, batch_predictions])

# 计算acc
if y_test is not None:
    print y_test[1]
    correct_pred = float(sum(all_predictions == y_test)) / float(len(y_test))
    print "ACC:", correct_pred

import cPickle
def save_conll_result():
    dic_all_res = {}
    demo = []
    print '测试数量:', len(x_test),len(x_raw),len(all_predictions)
    for i in range(len(x_test)):
        word = ''.join(x_raw[i].split(' '))
        #dic_all_res.setdefault(word, all_predictions[i])
        demo.append((word, all_predictions[i]))
    print '写入数量：',len(dic_all_res.keys())
    #with open('conll_test.dat','wb') as hdl:
    #    cPickle.dump(all_predictions, hdl)
    with open('temp.dat','wb') as temp_hdl:
        cPickle.dump(demo,temp_hdl)
    with open('y_test.dat','wb') as y_hdl:
        cPickle.dump(y_test, y_hdl)
    print 'Finish'
    
save_conll_result()
