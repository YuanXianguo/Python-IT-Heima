import multiprocessing
import time


def rec_msg(q):
    data = [i for i in range(10)]
    for d in data:
        q.put(d)
        time.sleep(0.4)
        print(q.qsize())

    print("下载结束".center(50, "-"))


def analysis(q):
    data = []
    while True:
        time.sleep(0.5)
        d = q.get()
        data.append(d)
        print("当前数据获取进度：{}".format(data))
        if q.empty():
            break


def main():
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=rec_msg, args=(q, ))
    p2 = multiprocessing.Process(target=analysis, args=(q, ))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
