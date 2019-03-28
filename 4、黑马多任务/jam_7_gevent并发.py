import gevent

from gevent import socket, monkey
monkey.patch_all()  # 对代码进行修订


def handle_requset(new_socket):
    while True:
        data = new_socket.recv(1024)  # 耗时操作，gevent将会切换
        if data:
            print("收到{}".format(data.decode("utf-8")))
            new_socket.send(data)
        else:
            new_socket.close()
            break


def server():
    gevent_server = socket.socket()
    gevent_server.bind(("", 1080))
    gevent_server.listen(128)
    while True:
        new_socket, new_adr = gevent_server.accept()  # 耗时操作，gevent将会切换
        gevent.spawn(handle_requset, new_socket)


if __name__ == '__main__':
    server()


