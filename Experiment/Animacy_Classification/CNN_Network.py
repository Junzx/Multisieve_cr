# coding:utf-8
import tensorflow as tf
import numpy as np
import gensim

def load_char_embedding():
    char_path = 'char_embedding_300d_5iter.model'
    return gensim.models.Word2Vec.load(char_path)

char_emb_moedl = load_char_embedding()


class CNN(object):
    def __init__(self, cnn_para):
        """
        :param cnn_para:装在CNN网络的参数，是个tuple
        """
        print('创建CNN网络中......')
        print 'CNN参数设置：'
        print 'seq_length:', cnn_para[0]
        print 'num_classes', cnn_para[1]
        print 'vocab_size:', cnn_para[2]

        sequence_length = cnn_para[0]
        num_classes = cnn_para[1]
        vocab_size = cnn_para[2]
        embedding_size = cnn_para[3]
        filter_sizes = cnn_para[4]
        num_filters = cnn_para[5]
        l2_reg_lambda = cnn_para[6]
        vocab_processor = cnn_para[7]

        # 构建输入输出层、dropout
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name = 'input_x')
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name = 'input_y')
        self.dropout_keep_prob = tf.placeholder(tf.float32, name = "dropout_keep_prob")

        # 定义l2 loss
        l2_loss = tf.constant(0.0)

        # 定义char embedding层
        with tf.device('/cpu:0'), tf.name_scope('embedding'):
            all_char_emb = [np.random.rand(300)]    # 初始化，必须先放进去一个，作为UNK
            for k, v in vocab_processor.vocabulary_._mapping.items():
                try:
                    char_emb = list(char_emb_moedl[k])
                except KeyError:
                    char_emb = list(np.random.rand(300))
                all_char_emb.append(char_emb)
            all_char_emb = np.array(all_char_emb)   # 每个字都被用一个300d的数组表示

            # TODO:这干嘛
            self.W = tf.Variable(all_char_emb, name = "W", dtype = tf.float32)
            self.embedding_chars = tf.nn.embedding_lookup(self.W, self.input_x)
            self.embedding_chars_expanded = tf.expand_dims(self.embedding_chars, -1)    # 添加一维

            # test
            tess = tf.Session()
            tess.run(tf.global_variables_initializer())
            print self.input_x.shape
            print self.input_y.shape
            print self.W.shape
            print self.embedding_chars.shape
            print self.embedding_chars_expanded

        # 定义卷积&池化层
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):

                # 卷积
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1, name = "W"))
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")

                conv = tf.nn.conv2d(
                    self.embedding_chars_expanded,
                    W,
                    strides = [1,1,1,1],
                    padding = "VALID",
                    name = "conv"
                )

                # 激活
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name = "relu")

                # 池化
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1,1,1,1],
                    padding="VALID",
                    name="pool"
                )
                pooled_outputs.append(pooled)

        # 结合所有的池化特征
        num_filters_total = num_filters * len(filter_sizes) # 2个卷积核，3个卷积，因此产生6维的向量 #update:说的不对，这里是128 * 3 = 384
        self.h_pool = tf.concat(pooled_outputs, 3)  # TODO:what??
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total]) # -1表示这个维度不指定，由程序自己计算生成

        # 添加dropout
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)

        # TODO：定义输出层？ | 最终（未正则化）的分数&预测
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer()
            )
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]),name = "b")
            l2_loss += tf.nn.l2_loss(W) # 返回的是一个数值
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores") # TODO:what's this
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # 计算交叉熵 # TODO:看懂这几个函数的意思
        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(
                logits=self.scores,
                labels=self.input_y
            )
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        # 精确度 # TODO: reduce mean
        with tf.name_scope("Accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

        print('Create CNN network success!')





if __name__ == '__main__':
    test = load_char_embedding()
    
