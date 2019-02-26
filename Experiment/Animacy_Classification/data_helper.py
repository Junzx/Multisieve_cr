# coding:utf-8
import numpy as np
import itertools
import parameters
from collections import Counter

def load_data_and_labels(tuple_datas):
    """
    读取数据
    """
    classes = np.eye(len(tuple_datas))  # 根据传入数据的种类，构建单元矩阵
    def __load_one_file(file_path):
        #example = list(open(file_path, 'r', encoding='utf-8').readlines())
        example = list(open(file_path, 'r').readlines())
        return [__add_space(word.strip()) for word in example]

    def __add_space(one_str):
        one_str = one_str.decode('utf-8')
        return ' '.join(list(one_str))

    # 最终返回的对象
    x_ = []
    y_ = []

    for file_index, file_path in enumerate(tuple_datas):
        print '读取：',
        print(file_path, classes[file_index])
        data = __load_one_file(file_path)
        x_.extend(data)
        for _ in range(len(data)):
            y_.append(classes[file_index])

    assert len(x_) == len(y_)
    return [x_, y_]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    print len(data)
    print 'fdffdfdsfds',data[1]
    data_size = len(data)
    num_batches_per_epoch = int((len(data) - 1)/batch_size) + 1 # 每个epoch有多少个batch
    print 'shit',num_batches_per_epoch
    print 'length', data_size
    for epoch in range(num_epochs):
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data

        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)    # 如果end index超过了最大，则选择最大的那个
            yield shuffled_data[start_index: end_index]


if __name__ == '__main__':
    tuple_data = (parameters.FLAGS.human_data_file, parameters.FLAGS.non_human_data_file)
    x,y = load_data_and_labels(tuple_data)
    print('-=-=-=-=-=-=-=-=-=-=-=-=')
    batches = batch_iter(list(zip(x,y)), 16, 200)
    print type(batches)
