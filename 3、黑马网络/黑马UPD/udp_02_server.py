from udp_tools import *


def server():
    """服务端"""

    # 创建并绑定套接字
    udp_socket = create_bind_socket(server_adr)
    print("开始监听。。。")

    while True:

        opt = eval(input("选择功能（1-发送，2-接收，0-退出）："))

        if opt == 1:
            # 发送消息
            send_datas(udp_socket, client_adr)
        elif opt == 2:
            # 接收消息
            receive_datas(udp_socket)
        elif opt == 0:
            break
        else:
            print("输入错误！")

    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    server()
