import socket
import re
import multiprocessing
from mini_frame import application


class WSGIServer(object):
    def __init__(self):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind(("", 1080))
        self.tcp_server_socket.listen(128)

    def service_client(self, server):
        recv_data = server.recv(1024).decode("utf-8")
        request_list = recv_data.splitlines()
        ret = re.match(r"[^/]+(/[^ ]*)", request_list[0])
        file = ""
        if ret:
            file = ret.group(1)
            if file == "/":
                file = "/index.html"
        if not file.endswith(".py"):
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
        else:
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "\r\n"

            response_body = application(file)

        response = response_header + response_body

        server.send(response.encode("utf-8"))
        server.close()

    def run_forever(self):
        while True:
            new_server, new_adr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.service_client, args=(new_server,))
            p.start()
            new_server.close()


if __name__ == '__main__':
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()
