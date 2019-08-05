import os

pid = os.fork()

if pid < 0:
    print('false')
elif pid == 0:
    # 获取当前进程pid
    print('child get pid', os.getpid())
    print('child get parent pid', os.getppid())
else:
    print('parent get child pid', pid)
    print('parent get pid', os.getpid())
