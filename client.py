from socket import *
import sys
import os
from time import sleep


# create socket 登录 创建子进程
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    s = socket(AF_INET, SOCK_DGRAM)

    while True:
        name = input('input your name:')
        msg = 'L '+name
        s.sendto(msg.encode(), ADDR)

        # waiting server message
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('登录成功')
            break
        else:
            print(data.decode())

    #   创建父子进程
    pid = os.fork()
    if pid < 0:
        sys.exit('创建子进程失败')
    elif pid == 0:
        p = os.fork()
        if p < 0:
            print('create process false')
        elif p == 0:
            send_msg(s, addr, name)
        else:
            os._exit(0)
    else:
        recv_msg(s)


def send_msg(s, addr, name):
    while True:
        sleep(0.5)
        try:
            text = input('say:')
            if text.strip() == 'quit':
                msg = 'Q '+name
                s.sendto(msg.encode(), addr)
                sys.exit('退出聊天室')

            msg = 'C %s %s' % (name, text)
            s.sendto(msg.encode(), addr)
        except KeyboardInterrupt:
            msg = 'Q '+name
            s.sendto(msg.encode(), addr)
            sys.exit('退出聊天室')




def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode()+'\nsay:', end='')


if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit(0)
