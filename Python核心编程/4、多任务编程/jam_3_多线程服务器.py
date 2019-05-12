import socket
import threading
import time


def rec_msg(new_socket, adr):
    while True:
        rec_data = new_socket.recv(1024)
        print("收到：{}，来自{}\n".format(rec_data.decode("utf-8"), adr))


def send_msg(new_socket):
    while True:
        send_data = input("输入：").encode("utf-8")
        new_socket.send(send_data)


def thread_server(new_socket, adr):
    while True:
        rec_data = new_socket.recv(1024)
        if rec_data:
            print("收到：{}，来自{}\n".format(rec_data.decode("utf-8"), adr))
            send_data = input("输入：").encode("utf-8")
            new_socket.send(send_data)
        else:
            break

    new_socket.close()


def thread_server2(new_socket, adr):
    t1 = threading.Thread(target=rec_msg, args=(new_socket, adr))
    t1.start()
    t2 = threading.Thread(target=send_msg, args=(new_socket, ))
    t2.start()


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 1080))
    tcp_socket.listen(1024)
    try:
        while True:
            print("等待新客户的连接。。。")
            new_socket, new_adr = tcp_socket.accept()
            t = threading.Thread(target=thread_server, args=(new_socket, new_adr))
            t.start()

            # new_socket.close()
    finally:
        tcp_socket.close()


if __name__ == '__main__':
    main()
