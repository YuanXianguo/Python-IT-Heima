import socket
import multiprocessing
import re
import sys

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"
WSGI_ROOT_DIR = "./wsgipython/"


class HTTPServer(object):
    def __init__(self, port, app):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", port))
        self.app = app

    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket, client_adr = self.server_socket.accept()
            print("{}连接上了".format(client_adr))
            p = multiprocessing.Process(target=self.deal_client,
                                        args=(client_socket,))
            p.start()
            client_socket.close()

    def start_response(self, status, headers):
        server_headers = [
            ("Server", "My Server")
        ]
        self.response_start_line = "HTTP1.1" + status + "\r\n"
        response_headers = server_headers + headers
        self.response_headers = ""
        for key, value in response_headers:
            self.response_headers += "{}:{}\r\n".format(key, value)

    def deal_client(self, client_socket):
        """处理客户端请求"""
        request_data = client_socket.recv(1024).decode("utf-8")

        # 解析请求报文
        request_lines = request_data.split("\r\n")

        # 提取用户请求的文件名
        file_name = re.search(r"\w+\s+(/[^\s]*)\s+", request_lines[0]).group(1)
        method = re.search(r"(\w+)\s+(/[^\s]*)\s+", request_lines[0]).group(1)

        env = {
            "PATH_INFO": file_name,
            "METHOD": method
        }
        # 调用模块默认的WSGI接口函数
        response_body = self.app(env, self.start_response)

        response = (self.response_start_line
                    + self.response_headers
                    + "\r\n{}".format(response_body))

        client_socket.send(response.encode("utf-8"))
        client_socket.close()


def main():
    if len(sys.argv) < 2:
        sys.exit("python MyWebServer.py MyWebFramework:app")
    module_name, app_name = sys.argv[1].split(":")
    m = __import__(module_name)
    app = getattr(m, app_name)
    http_server = HTTPServer(8001, app)
    http_server.start()


if __name__ == '__main__':
    main()
