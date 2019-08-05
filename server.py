#!/usr/local/bin python3
# coding=utf-8
"""
introduce:Chat_room server
"""

from socket import *
import os
import sys


# 创建网络，创建进程，调用功能函数
def main():
    # server address
    ADDR = ('0.0.0.0', 8888)

    # create socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    # create process
    pid = os.fork()
    if pid < 0:
        sys.exit('create process false')
    elif pid == 0:
        p = os.fork()
        if p < 0:
            print('create process false')
        elif p == 0:
            do_child(s, ('127.0.0.1', 8888))
        else:
            os._exit(0)

    else:
        do_parent(s)


# 管理员喊话
def do_child(s, addr):
    while True:
        msg = input('管理员消息：')
        msg = 'C GM ' + msg
        s.sendto(msg.encode(), addr)


# 客户端请求
def do_parent(s):
    # {'zhangsan':("0.0.0.0", 8888)}
    user = {}
    while True:
        data, addr = s.recvfrom(1024)
        msglist = data.decode().split(' ')
        if msglist[0] == 'L':
            do_login(s, user, msglist[1], addr)
        elif msglist[0] == 'C':
            do_chat(s, user, msglist[1], ' '.join(msglist[2:]))
        elif msglist[0] == 'Q':
            do_quit(s, user, msglist[1])


def do_quit(s, user, name):
    # 退出聊天室
    msg = '\n' + name + '退出了聊天室'
    for i in user:
        if i == name:
            s.sendto('EXIT'.encode(), user[i])
        else:
            s.sendto(msg.encode(), user[i])
    # 从字典中删除用户
    del user[name]


def do_chat(s, user, name, text):
    msg = '\n%s 说 %s' % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


# 登录判断
def do_login(s, user, name, addr):
    if name in user or name == 'GM':
        s.sendto('用户存在'.encode(), addr)
        return
    s.sendto('OK'.encode(), addr)

    # 通知其他人
    msg = '\n欢迎%s进入聊天室' % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    user[name] = addr


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('服务器退出')