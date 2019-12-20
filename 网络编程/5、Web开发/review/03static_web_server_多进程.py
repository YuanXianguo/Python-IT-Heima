import socket
import re
import multiprocessing


def service_client(server):
    while True:
        recv_data = server.recv(1024).decode("utf-8")
        if not recv_data:
            break
        request_list = recv_data.splitlines()
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
    server.close()


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("", 1080))
    tcp_server_socket.listen(128)

    while True:
        new_server, new_adr = tcp_server_socket.accept()
        p = multiprocessing.Process(target=service_client, args=(new_server,))
        p.start()
        new_server.close()


if __name__ == '__main__':
    main()
