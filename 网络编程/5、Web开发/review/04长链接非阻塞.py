import socket
import re
import time


def service_client(server, rev_data):
    request_list = rev_data.splitlines()
    ret = re.match(r"[^/]+(/[^ ]*)", request_list[0])
    file = ""
    if ret:
        file = ret.group(1)
        if file == "/":
            file = "/index.html"
    try:
        with open("html" + file, "r", encoding="utf-8") as f:
            html_content = f.read()

        response_body = html_content

        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"

    except:
        response_body = "file not found"

        response_header = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"

    response = response_header + response_body

    server.send(response.encode("utf-8"))


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setblocking(False)  # 将套接字设置为非阻塞
    tcp_server_socket.bind(("", 1080))
    tcp_server_socket.listen(128)

    server_socket_list = list()  # 存储服务客户端的套接字的列表
    while True:
        try:
            new_server, addr = tcp_server_socket.accept()
        except:
            pass
        else:
            new_server.setblocking(False)
            server_socket_list.append(new_server)
        time.sleep(0.5)

        # 遍历服务客户端的套接字
        for server in server_socket_list:
            try:
                rev_data = server.recv(1024).decode("utf-8")
            except:
                pass
            else:
                if rev_data:
                    service_client(server, rev_data)
                else:  # 结阻塞为空，说明客户端关闭
                    server.close()
                    server_socket_list.remove(server)


if __name__ == '__main__':
    main()
