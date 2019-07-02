import os
import multiprocessing
import time


def copy_file(q, file, from_path, to_path):
    """复制单个文件"""
    with open(os.path.join(from_path, file), "rb") as f:
        content = f.read()
    with open(os.path.join(to_path, file), "wb") as f:
        f.write(content)

    q.put(file)


def main():
    from_path = input("输入要复制的文件夹：")
    # 获取原文件列表
    files = os.listdir(from_path)

    # 创建复件文件夹
    to_path = from_path + "[复件]"
    try:
        os.mkdir(to_path)
    except:
        pass

    # 创建进程间通信队列
    q = multiprocessing.Manager().Queue()

    # 创建进程池
    pool = multiprocessing.Pool(4)
    for file in files:
        pool.apply_async(copy_file, (q, file, from_path, to_path))

    pool.close()
    # pool.join()

    # 显示复制进度
    file_nums = len(files)
    cnt = 0
    while cnt < file_nums:
        time.sleep(0.1)
        file = q.get()
        cnt += 1

        per = cnt / file_nums * 100
        char = "*" * (int(per) // 2)
        print("\r复制进度：[{:-<50}>]{:.2f}%".format(char, per), end="")


if __name__ == '__main__':
    main()
