import socket
import re


def service_client(sock):
    request_msg = sock.recv(1024).decode("utf-8")
    msgs = request_msg.splitlines()
    print(msgs)
    file = ""
    ret = re.match(r"[^/]+(/[^ ]*)", msgs[0])
    if ret:
        file = ret.group(1)
        if file == "/":
            file = "/index.html"
    try:
        with open("html" + file, "r", encoding="utf-8") as f:
            send_msg = f.read()
        response_msg = "HTTP/1.1 200 OK\r\n"  # 第一行
        response_msg += "\r\n"  # 空行区分header和body
        response_msg += send_msg

        sock.send(response_msg.encode("utf-8"))
    except:
        response_msg = "HTTP/1.1 404 NOT FOUND\r\n"  # 第一行
        response_msg += "\r\n"  # 空行区分header和body
        response_msg += "file not found"

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
