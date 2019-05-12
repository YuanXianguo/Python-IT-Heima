import threading
from udp_tools import *


def server():
    udp_socket = create_bind_socket(server_adr)
    t_rec = threading.Thread(target=rec_msg, args=(udp_socket, ))
    t_send = threading.Thread(target=send_msg, args=(udp_socket, client_adr))
    t_rec.start()
    t_send.start()


if __name__ == '__main__':
    server()
