# encoding=utf-8
import ctypes
from getpass import getuser
from os import name, listdir, getcwd

if __name__ == '__main__':
    cilin_lib_path = getcwd() + '/libcilin.so'
    cilin_lib_data = getcwd() + '/dataset.txt'
else:
    # cilin_lib_path = getcwd() + '/libcilin.so'
    cilin_lib_path = './SubjectUtils/get_similarity' + '/libcilin.so'
    cilin_lib_data = './SubjectUtils/get_similarity' + '/dataset.txt'
    # cilin_lib_data = getcwd() + '/dataset.txt'


so = ctypes.cdll.LoadLibrary
cilin_lib = so(cilin_lib_path)
cilin_lib.read_cilin(cilin_lib_data)
cilin_lib.similarity.restype = ctypes.c_float

def get_similarity_API(word1,word2):
    """
    返回两个词语的相似度
    """
    return cilin_lib.similarity(word1,word2)

if __name__ == '__main__':
    print get_similarity_API('北京','首都')
    # pass
