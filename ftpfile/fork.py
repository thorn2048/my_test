import os
from time import sleep

a = 1
pid = os.fork()

if pid < 0:
    print('false')
elif pid == 0:
    print('old')
    print(a)
    a = 10000
else:
    sleep(1)
    print('new')
    print('a=', a)

print('over')
