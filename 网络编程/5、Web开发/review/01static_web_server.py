import socket


def service_client(sock):
    request_msg = sock.recv(1024)
    print(request_msg)

    response_msg = "HTTP/1.1 200 OK\r\n"  # 第一行
    response_msg += "\r\n"  # 空行区分header和body
    response_msg += "<h1>Hello World!<h1>"

    sock.send(response_msg.encode("utf-8"))

    sock.close()


def main():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_server.bind(("", 1080))

    tcp_server.listen(128)

    while True:
        new_client_sock, addr = tcp_server.accept()
        service_client(new_client_sock)

    # tcp_server.close()


if __name__ == '__main__':
    main()
