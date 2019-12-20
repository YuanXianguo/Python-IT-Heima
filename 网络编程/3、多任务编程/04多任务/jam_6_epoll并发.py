import select
import socket


def server():
    epoll_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    epoll_server.bind(("", 1080))
    epoll_server.listen(128)

    # 创建一个epoll对象
    epoll = select.epoll()

    # 将创建的套件字添加到epoll的事件监听中
    # epoll_server.fileno()得到epoll_server的文件描述符
    # select.EPOLLIN | select.EPOLLET，检测可接收数据事件，ET模式
    # LT：水平触发，每次都通知，ET，边缘触发，只通知一次
    epoll.register(epoll_server.fileno(), select.EPOLLIN | select.EPOLLET)

    clients = {}
    adrs = {}

    # 循环等待客户端的到来或者对方发送数据
    while True:

        # epoll进行fd扫描的地方，未指定超时时间则为阻塞等待
        epoll_list = epoll.poll()

        # 对事件进行判断
        for fd, events in epoll_list:
            # 如果是socket创建的套接字被激活
            if fd == epoll_server.fileno():
                new_client, new_adr = epoll_server.accept()
                print("有新的客户端{}到来".format(new_adr))
                # 将新信息保存下来
                clients[new_client.fileno()] = new_client
                adrs[new_client.fileno()] = new_adr

                # 将新客户端向epoll中注册
                epoll.register(new_client.fileno(),
                               select.EPOLLIN | select.EPOLLET)

            # 判断事件是否是可接收数据的事件
            elif events == select.EPOLLIN:
                rec_data = clients[fd].recv(1024)
                if rec_data:
                    print("收到{}，来自{}".format(rec_data.decode("utf-8"),
                                             adrs[fd]))
                else:
                    # 从epoll中移除该连接fd
                    epoll.unregister(fd)
                    clients[fd].close()


if __name__ == '__main__':
    server()
