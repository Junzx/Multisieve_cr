import cPickle
def test():
    with open('all_result.test', 'rb') as hdl:
        all_res = cPickle.load(hdl)

    for key in all_res:
        if key == 'counter':
            continue
        print key, '    ',
        print all_res[key] / all_res['counter']
    print '-' * 30

if __name__ == '__main__':
    test()