from attribute_classification_utils import make_metrix, load_model, load_file
import numpy as np

test_human = './test_human.txt'
test_non_human = './test_non_human.txt'

lst_test_human = load_file(test_human)
lst_test_non_human = load_file(test_non_human)

x_test = np.array([i for i in make_metrix(lst_test_human)] + [i for i in make_metrix(lst_test_non_human)])
y_test = np.array([i for i in np.zeros(len(lst_test_human))] + [i for i in np.ones(len(lst_test_non_human))])


test_male = './test_male.txt'
test_female = './test_female.txt'

lst_test_male = load_file(test_male)
lst_test_female = load_file(test_female)

x_test_gender = np.array([i for i in make_metrix(lst_test_male)] + [i for i in make_metrix(lst_test_female)])
y_test_gender = np.array([i for i in np.zeros(len(lst_test_male))] + [i for i in np.ones(len(lst_test_female))])
