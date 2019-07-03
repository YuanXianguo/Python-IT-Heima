import sys
import socket
import re
import multiprocessing


class WSGIServer(object):
    def __init__(self, port, app, config):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind(("", port))
        self.tcp_server_socket.listen(128)
        self.headers = "HTTP/1.1 "
        self.application = app
        self.config = config

    def get_response(self, status, headers):
        self.headers += status + "\r\n"
        for header in headers:
            self.headers += "{}:{}\r\n".format(header[0], header[1])

        self.headers += "\r\n"

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
                with open(self.config["static_path"] + file, "r", encoding="utf-8") as f:
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

            env = dict()
            env["file"] = file
            response_body = self.application(env, self.get_response)
            response_header = self.headers

        response = response_header + response_body

        server.send(response.encode("utf-8"))
        server.close()

    def run_forever(self):
        while True:
            new_server, new_adr = self.tcp_server_socket.accept()
            p = multiprocessing.Process(target=self.service_client, args=(new_server,))
            p.start()
            new_server.close()


def main():
    if len(sys.argv) == 3:
        try:
            port = int(sys.argv[1])
        except:
            print("端口输入错误")
            return
    else:
        print("请按照以下方式运行：")
        print("python web_server.py 1080 mini_frame:application")
        return

    # 解析路径
    with open("./web_server.conf", "r") as f:
        conf_info = eval(f.read())

    # 解析模块和函数
    ret = re.match(r"([^:]+):(.*)", sys.argv[2])
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)

        # 动态导入模块
        sys.path.append(conf_info["dynamic_path"])
        frame = __import__(frame_name)
        app = getattr(frame, app_name)

        wsgi_server = WSGIServer(port, app, conf_info)
        wsgi_server.run_forever()
    else:
        print("请按照以下方式运行：")
        print("python web_server.py 1080 mini_frame:application")
        return


if __name__ == '__main__':
    main()
