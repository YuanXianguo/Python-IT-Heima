import multiprocessing
import os
import time


def copy(f_path, t_path, f_name, q):
    with open(os.path.join(f_path, f_name), "r", encoding="utf-8") as f:
        file = f.read()
    with open(os.path.join(t_path, f_name), "w", encoding="utf-8") as f:
        f.write(file)

    q.put(f_name)


def main():
    f_path = (input("输入要复制的文件夹："))
    t_path = f_path + "[复件]"

    try:
        os.mkdir(t_path)
    except Exception as r:
        print(r)

    f_names = os.listdir(f_path)

    q = multiprocessing.Manager().Queue()

    pool = multiprocessing.Pool(4)
    for f_name in f_names:
        pool.apply_async(copy, args=(f_path, t_path, f_name, q))

    pool.close()
    # pool.join()

    count = 0
    while True:
        time.sleep(0.1)
        f_name = q.get()
        # print("完成copy：{}".format(f_name))
        count += 1

        per = count * 100 // len(f_names)
        char = "=" * (per // 2) + ">"
        print("\r进度：[{:-<51}]{:.2f}%".format(char, per), end="")

        if count >= len(f_names):
            break


if __name__ == '__main__':
    main()
