import os



with open('sizetest.txt', 'w') as fp:
    fp.write('hello')

statinfo = os.stat('sizetest.txt')
print statinfo
print statinfo.st_size