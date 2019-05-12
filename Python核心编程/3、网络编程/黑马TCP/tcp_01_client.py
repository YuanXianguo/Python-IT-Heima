import socket


def client():

    # 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 链接服务器
    tcp_socket.connect(("192.168.21.29", 1080))

    while True:

        # 发送数据
        send_data = input("输入内容：")
        if send_data in ['q', '']:
            break
        tcp_socket.send(send_data.encode("utf-8"))

        # 接收数据
        rec_data = tcp_socket.recv(1024).decode("utf-8")
        print("收到回复：{}".format(rec_data))

    # 关闭套接字
    tcp_socket.close()


if __name__ == '__main__':
    client()
