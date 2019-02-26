# coding:utf-8
import tensorflow as tf
import os

#checkpoint = '1536634590' # 实验1.1
#checkpoint = '1536637654' # 实验1.2
#checkpoint = '1536643797' # 实验1.3
#checkpoint = '1536647365' # 实验2.1
checkpoint = '1536652635'
#checkpoint = '1536590221' # 选择所有的训练数据
#checkpoint = '1536629912'

tf.flags.DEFINE_float("dev_sample_percentage",.1,u"用于评测的训练数据的百分比")
#tf.flags.DEFINE_string("human_data_file", "./data/train/train_human.txt", "human txt") # 实验2
tf.flags.DEFINE_string("human_data_file","./data/train/human_tongyici.txt","provided by tech.")  # 实验3
#tf.flags.DEFINE_string("human_data_file","./data/train/train_human_test.txt"," org + teach")   # 实验1
tf.flags.DEFINE_string("non_human_data_file", "./data/train/train_non_human.txt", "human txt")
tf.flags.DEFINE_string("human_test_data","./data/test/test_human.txt","human test")
tf.flags.DEFINE_string("non_human_test_data", "./data/test/test_non_human.txt","non human test")

tf.flags.DEFINE_integer("embedding_dim", 300, "dim of embedding")
tf.flags.DEFINE_string("filter_sizes", "2,3,4", "filter sizes")
tf.flags.DEFINE_integer("num_filters", 128, "number of filters per filter size")    # 卷积核数目
tf.flags.DEFINE_float("dropout_keep_prob", 0.8, "dropout")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "l2 reg")

# 训练时参数
tf.flags.DEFINE_integer("batch_size", 16, "batch size")
tf.flags.DEFINE_integer("num_epochs", 200, "epoch")
tf.flags.DEFINE_integer("evaluate_every", 100, u"每100次就在dev数据上纪念性测试")
tf.flags.DEFINE_integer("checkpoint_every", 100, "save model after this man steps")
tf.flags.DEFINE_integer("num_checkpoints", 5, "save 5 checkpoints")

# 测试时参数
tf.flags.DEFINE_string("checkpoint_dir",os.getcwd() + "/runs/" + checkpoint + "/checkpoints","checkpoint")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", False, "allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "log placement of ops on devices")

FLAGS = tf.flags.FLAGS
