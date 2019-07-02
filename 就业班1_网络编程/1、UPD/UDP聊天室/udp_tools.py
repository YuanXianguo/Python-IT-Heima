import socket

client_adr = ("192.168.21.36", 1080)
server_adr = ("192.168.21.36", 1060)


def create_bind_socket(adr):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(adr)
    return udp_socket


def send_msg(udp_socket, adr):
    while True:
        send_data = input("发送：").encode("utf-8")
        udp_socket.sendto(send_data, adr)


def rec_msg(udp_socket):
    while True:
        rec_data = udp_socket.recvfrom(1024)
        print("\n收到：'{}'，来自{}".format(
            rec_data[0].decode("utf-8"), rec_data[1]))


