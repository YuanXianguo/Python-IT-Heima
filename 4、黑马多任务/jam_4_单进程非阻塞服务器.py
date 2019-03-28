import socket


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)  # 设置为非阻塞
    server_socket.bind(("", 1080))
    server_socket.listen(1024)
    socket_list = []
    while True:
        try:
            new_socket, new_adr = server_socket.accept()
        except:
            pass
        else:
            print("一个新客户端{}到来".format(new_adr))
            new_socket.setblocking(False)
            socket_list.append((new_socket, new_adr))
        for socket_, adr in socket_list:
            try:
                rec_data = socket_.recv(1024)
            except:
                pass
            else:
                if rec_data:
                    print("收到{}，来自{}".format(
                        rec_data.decode("utf-8"), adr))
                else:
                    socket_.close()
                    socket_list.remove((socket_, adr))
                    print("{}已经下线".format(adr))


if __name__ == '__main__':
    server()
