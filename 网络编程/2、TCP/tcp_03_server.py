import socket


def server():
    """循环服务多个客户"""

    # 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定套接字
    tcp_server_socket.bind(("", 1080))

    # 将套接字设置为监听
    tcp_server_socket.listen(128)

    while True:
        # 等待客户端连接，返回值为为该客户端新建的通信套接字和客户端地址
        # 阻塞模式，直到收到客户端连接
        print("开始监听，等待客户端连接。。。")
        client_socket, client_adr = tcp_server_socket.accept()
        print("收到 {} 的连接".format(client_adr))

        # 等待接收客户端数据
        rec_data = client_socket.recv(1024).decode("utf-8")
        print("收到 {} 的信息：{}".format(client_adr, rec_data))

        # 发送回复
        send_data = input("回复：").encode("utf-8")
        client_socket.send(send_data)

        client_socket.close()
    # tcp_server_socket.close()


if __name__ == '__main__':
    server()


