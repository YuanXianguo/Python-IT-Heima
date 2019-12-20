import socket
import threading
from collections import deque
from datetime import datetime

from app import app
from my_sql import PyMySQL


def client(q):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("192.168.124.10", 520))
    # client_sock.connect(("127.0.0.1", 1080))

    while True:
        try:
            client_sock.send("TR0\r\n".encode("utf-8"))
            rec_data = client_sock.recv(1024).decode("utf-8")
            q.append(rec_data)
        except:
            pass


def insert(q):
    mysql = PyMySQL("localhost", 3306, "root", "pwd", "baogang")
    while True:
        if q:
            rec_data = q.popleft()
            rec_data_list = rec_data.split("$")[1:]
            rec_data_list.append(rec_data_list.pop(2))
            rec_data_list.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            try:
                sql = "select work_id from pictures where id=1"
                res = mysql.get_one(sql, ())[0]
            except:
                res = ""
            rec_data_list.append(res)
            sql = "insert into pictures (" \
                  "gray0, gray1, gray2, gray3, gray4, gray5, gray6, gray7, gray8, gray9, " \
                  "path, time, work_id) values (" \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            mysql.insert(sql, tuple(rec_data_list))
            print(rec_data_list)

            sql = "update pictures set gray0=%s, gray1=%s, gray2=%s,gray3=%s, gray4=%s, gray5=%s," \
                  "gray6=%s, gray7=%s, gray8=%s,gray9=%s, path=%s,time=%s where id=1"
            mysql.update(sql, tuple(rec_data_list[:-1]))


def main(q):
    t1 = threading.Thread(target=client, args=(q,))
    t2 = threading.Thread(target=insert, args=(q,))
    t1.start()
    t2.start()


if __name__ == '__main__':
    import multiprocessing
    q = deque()

    p = multiprocessing.Process(target=main, args=(q,))
    p.start()
    # main(q)
    app.run()

