import socket
import multiprocessing
import re

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8001))
    server_socket.listen(128)
    while True:
        client_socket, client_adr = server_socket.accept()
        print("{}连接上了".format(client_adr))
        p = multiprocessing.Process(target=deal_client, args=(client_socket, ))
        p.start()
        client_socket.close()


def deal_client(client_socket):
    """处理客户端请求"""
    request_data = client_socket.recv(1024).decode("utf-8")

    # 解析请求报文
    request_lines = request_data.split("\r\n")

    # 提取用户请求的文件名
    print(request_lines)
    file_name = re.search(r"\w+\s+(/[^\s]*)\s+", request_lines[0]).group(1)

    # 打开文件，读取内容
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
    print("response_data:{}".format(response))

    client_socket.send(response.encode("utf-8"))
    client_socket.close()


if __name__ == '__main__':
    server()
