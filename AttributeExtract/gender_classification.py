# coding: utf-8
import attribute_classification_utils
import config
import numpy as np
from attribute_classification_utils import make_metrix, save_model, load_model
from sklearn import linear_model
from sklearn import svm

from sklearn.model_selection import cross_val_score

train_male = './train_male.txt'
train_female = './train_female.txt'

lst_train_male = attribute_classification_utils.load_file(train_male)
lst_train_female = attribute_classification_utils.load_file(train_female)

x_train = np.array([i for i in make_metrix(lst_train_male)] + [i for i in make_metrix(lst_train_female)])
y_train = np.array([i for i in np.zeros(len(lst_train_male))] + [i for i in np.ones(len(lst_train_female))])


print 'load animacy data!'

lr_model = linear_model.LogisticRegression()
# svm_model = svm.SVC()

scores=cross_val_score(lr_model,x_train,y_train,cv=5)
print '准确率',np.mean(scores),scores

save_model('animacy_lr.model', lr_model)