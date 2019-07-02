import socket

server_adr = ("192.168.21.29", 1080)  # 服务端地址
client_adr = ("192.168.21.29", 1060)  # 客户都地址


def create_bind_socket(adr):
    """创建并绑定套接字"""

    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定一个本地信息
    udp_socket.bind(adr)

    return udp_socket


def receive_datas(udp_socket):
    """接收并显示数据"""

    # 使用套接字接收数据：（接收到的数据，（发送方的ip,port））
    rec_data = udp_socket.recvfrom(1024)
    rec_msg = rec_data[0].decode("utf-8")
    rec_adr = rec_data[1]

    # 显示接收到的数据
    if rec_msg:
        print("接受到 {} 的数据：{}".format(rec_adr, rec_msg))


def send_datas(udp_socket, adr):
    """发送数据"""

    send_data = input("输入内容：").encode("utf-8")
    udp_socket.sendto(send_data, adr)

