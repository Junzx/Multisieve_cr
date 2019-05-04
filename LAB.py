global a
a = 10
print id(a)
def test():
    a = 2
    print 'in func'
    print a
    print id(a)

print 'before:',a, id(a)
test()
print 'after:', a, id(a)