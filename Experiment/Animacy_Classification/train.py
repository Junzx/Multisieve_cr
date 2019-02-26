# coding:utf-8
import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helper
import parameters
from CNN_Network import CNN
from tensorflow.contrib import learn

os.environ["CUDA_VISIBLE_DEVICES"]="-1"
# 定义参数
FLAGS = parameters.FLAGS
tuple_datas = (FLAGS.human_data_file, FLAGS.non_human_data_file)

def preprocess():
    """
    切分数据
    """
    x_, y_ = data_helper.load_data_and_labels(tuple_datas)

    # 构建词典
    max_document_length = max([int(len(x.split(" ")))for x in x_])  # 23
    print '最大长度：', max_document_length
    vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
    x = np.array(list(vocab_processor.fit_transform(x_)))

    np.random.seed(100)
    shuffle_indices = np.random.permutation(len(y_))
    x_shuffled = np.array(x)[shuffle_indices]
    y_shuffled = np.array(y_)[shuffle_indices]

    dev_sample_index = -1 * int(FLAGS.dev_sample_percentage * float(len(y_)))

    x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
    y_train, y_dev = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]

    del x, y_, x_shuffled, y_shuffled
    return (x_train, y_train, x_dev, y_dev, vocab_processor)




def train(x_train, y_train, x_dev, y_dev, vocab_processor):
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement = FLAGS.allow_soft_placement, # 是否打印设备日志
            log_device_placement = FLAGS.log_device_placement, # 若指定的设备不存在，是否允许自动分配设备
        )
        sess = tf.Session(config=session_conf)

        with sess.as_default():
            cnn_para = (
                x_train.shape[1],
                y_train.shape[1],   # num_classes, 2
                len(vocab_processor.vocabulary_), # vocab_size
                FLAGS.embedding_dim,    # emb size
                list(map(int, FLAGS.filter_sizes.split(','))),
                FLAGS.num_filters,  # 128
                FLAGS.l2_reg_lambda,
                vocab_processor
            )
            cnn = CNN(cnn_para)

        global_step = tf.Variable(0, name = "global_step", trainable = False)   # 这里trainable是false

        # 定义优化器
        optimizer = tf.train.AdamOptimizer(1e-3)    # 括号内是学习率，使用ADAM优化器
        grads_and_vars = optimizer.compute_gradients(cnn.loss)  # 计算梯度
        train_op = optimizer.apply_gradients(grads_and_vars, global_step = global_step) # 应用梯度
        print '梯度长度：',len(grads_and_vars)
        for i in grads_and_vars:
            print '梯度：',
            for t in i:
                print t.name, '|',
            print
        print '-=-=' * 5
        
        # 输出的文件夹
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, 'runs', timestamp))
        print '输出文件夹：', out_dir

        # checkpoint 目录
        checkpoint_dir = os.path.abspath(os.path.join(out_dir,'checkpoints'))
        checkpoint_prefix = os.path.join(checkpoint_dir,'model')
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep = FLAGS.num_checkpoints)  # 保存器
        
        # 写入字典
        vocab_processor.save(os.path.join(out_dir, "vocab"))

        # 初始化向量
        sess.run(tf.global_variables_initializer())
        
        def train_step(x_batch, y_batch):
            feed_dict = {
                   cnn.input_x: x_batch,    # 对应placeholder
                   cnn.input_y: y_batch,
                   cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
                   }

            temp, step, loss, accuracy = sess.run(
                    [train_op, global_step, cnn.loss, cnn.accuracy],
                    feed_dict
                    )
            time_str = datetime.datetime.now().isoformat()
            print time_str, step, loss,accuracy

        # 创建batch
        batches = data_helper.batch_iter(
                    list(zip(x_train, y_train)),
                    FLAGS.batch_size,
                    FLAGS.num_epochs
                )
        for batch in batches:
            x_batch, y_batch = zip(*batch)
            train_step(x_batch, y_batch)
            current_step = tf.train.global_step(sess, global_step)
            
            if current_step % FLAGS.checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                print 'save the checkpoint to:   ',path





def main():
    x_train, y_train, x_dev, y_dev, vocab_processor = preprocess()
    train(x_train, y_train, x_dev, y_dev, vocab_processor)

if __name__ == '__main__':
    main()
