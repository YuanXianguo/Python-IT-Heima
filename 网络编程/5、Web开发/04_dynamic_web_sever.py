import socket
import multiprocessing
import re
import sys

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"
WSGI_ROOT_DIR = "./wsgipython/"


class HTTPServer(object):
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", port))

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
        if file_name.endswith(".py"):
            try:
                m = __import__(file_name[1:-3])  # 导入用户请求的模块
            except:
                self.response_start_line = "HTTP1.1 404 Not Found"
                self.response_headers = "\r\n"
                response_body = "not found"
            else:
                env = {
                    "PATH_INFO": file_name,
                    "METHOD": method
                }
                # 调用模块默认的WSGI接口函数
                response_body = m.application(env, self.start_response)

            response = (self.response_start_line
                        + self.response_headers
                        + "\r\n{}".format(response_body))

        else:  # 打开静态文件，读取内容
            try:
                with open(HTML_ROOT_DIR + file_name, "r", encoding="utf-8") as f:
                    data = f.read()
            except:  # 文件不存在，打开默认的文件
                with open(HTML_ROOT_DIR + "/index.html", "r", encoding="utf-8") as f:
                    data = f.read()

            response_start_line = "HTTP1.1 200 OK\r\n"
            response_headers = "Server: My Server\r\n"
            response_body = "\r\n{}".format(data)
            response = response_start_line + response_headers + response_body

        client_socket.send(response.encode("utf-8"))
        client_socket.close()


def main():
    sys.path.insert(1, WSGI_ROOT_DIR)
    server = HTTPServer(8001)
    server.start()


if __name__ == '__main__':
    main()
