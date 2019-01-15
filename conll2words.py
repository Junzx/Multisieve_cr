import config
import os
import LoadConll

def conll2sent(file_):
    obj_data = LoadConll.load_one_file(file_)
    token_list = []
    label_list = []
    for token in obj_data.lst_tokens:
        token_list.append(token.word_itself)
        if token.np_info == '-':
            label_list.append(False)
        else:
            label_list.append(True)

    return token_list, label_list

if __name__ == '__main__':
    # print os.listdir(config.basic_folder + config.gold_train)
    print os.listdir(os.getcwd())
    from pprint import pprint
    test_ = 'test.v4_gold_conll'
    pprint(conll2sent(test_))


