import os
import time
from multiprocessing import Pool


def copy_files(r_path, w_path):
    try:
        with open(r_path, 'r', encoding='utf-8') as f:
            text = f.read()
        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as result:
        print(result)


def copy(from_path, to_path, file_list):
    for file_name in file_list:
        copy_files(os.path.join(from_path, file_name),
                   os.path.join(to_path, file_name))


def copy_pool(from_path, to_path2, file_list):
    pool = Pool(8)
    for file_name in file_list:
        pool.apply_async(copy_files, args=(os.path.join(from_path, file_name),
                                           os.path.join(to_path2, file_name)))
    pool.close()
    pool.join()  # 等待所有进程结束


def main():
    from_path = r'E:\GitHub\Python-Project-Development\demo'
    to_path = '../test'
    to_path2 = '../test2'
    try:
        os.mkdir(to_path)
        os.mkdir(to_path2)
    except:
        pass

    # 读取from_path下所有的文件
    file_list = os.listdir(from_path)

    # 单进程复制时间
    start = time.perf_counter()
    copy(from_path, to_path, file_list)
    end1 = time.perf_counter()

    # 多进程复制时间
    copy_pool(from_path, to_path2, file_list)
    end2 = time.perf_counter()

    print('单进程复制耗时：{:.2f}\n多进程复制耗时：{:.2f}'.format(
        end1 - start, end2 - end1))


if __name__ == '__main__':
    main()
