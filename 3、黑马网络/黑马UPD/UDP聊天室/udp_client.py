import threading
from udp_tools import *


def client():
    udp_socket = create_bind_socket(client_adr)
    t_send = threading.Thread(target=send_msg, args=(udp_socket, server_adr))
    t_rec = threading.Thread(target=rec_msg, args=(udp_socket, ))
    t_send.start()
    t_rec.start()


if __name__ == '__main__':
    client()
