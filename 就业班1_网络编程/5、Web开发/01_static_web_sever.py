import socket
import multiprocessing


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
    print("request_data:{}".format(request_data))

    response_start_line = "HTTP1.1 200 OK\r\n"
    response_headers = "Server: My Server\r\n"
    response_body = "\r\nhello itcast"
    response = response_start_line + response_headers + response_body
    print("response_data:{}".format(response))

    client_socket.send(response.encode("utf-8"))
    client_socket.close()


if __name__ == '__main__':
    server()
