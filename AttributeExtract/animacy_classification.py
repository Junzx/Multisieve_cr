# coding: utf-8
import attribute_classification_utils
import config
import numpy as np
from attribute_classification_utils import make_metrix, save_model, load_model
from sklearn import linear_model
from sklearn import svm

from sklearn.model_selection import cross_val_score

train_human = './train_human.txt'
train_non_human = './train_non_human.txt'

lst_train_human = attribute_classification_utils.load_file(train_human)
lst_train_non_human = attribute_classification_utils.load_file(train_non_human)

x_train = np.array([i for i in make_metrix(lst_train_human)] + [i for i in make_metrix(lst_train_non_human)])
y_train = np.array([i for i in np.zeros(len(lst_train_human))] + [i for i in np.ones(len(lst_train_non_human))])



print 'load animacy data!'

lr_model = linear_model.LogisticRegression()
# svm_model = svm.SVC()

scores=cross_val_score(lr_model,x_train,y_train,cv=5)
print '准确率',np.mean(scores),scores

save_model('animacy_lr.model', lr_model)