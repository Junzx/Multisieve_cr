import api_cr_one_file
import LoadConll
from SubjectUtils.unit_test_utils import print_cluster

test = 'test.v4_gold_conll'

data = LoadConll.load_one_file(test)

api_cr_one_file.main(data)

print_cluster(data)