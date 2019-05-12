import select
import socket
import sys


def server():
    select_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    select_server.bind(("", 1080))
    select_server.listen(128)

    # 监听列表，32位机默认1024个上限，64位2048
    inputs = [select_server, sys.stdin]

    run_flag = True

    while True:
        # 调用select函数，阻塞等待
        readable, writeable, exceptional = select.select(inputs, [], [])

        # 数据抵达，循环读取
        for sock in readable:
            # 监听到有新的连接
            if sock == select_server:
                new_client, new_adr = select_server.accept()
                # 将新建立的套接字放入监听列表
                inputs.append(new_client)

            # 监听到有键盘输入
            elif sock == sys.stdin:
                cmd = sys.stdin.readline()
                run_flag = False
                break

            else:
                # 读取客户端连接发送的数据
                data = sock.rec(1024)
                if data:
                    sock.send(data)
                else:
                    # 客户已下线，移出套接字
                    inputs.remove(sock)
                    sock.close()
