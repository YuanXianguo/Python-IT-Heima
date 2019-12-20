import tensorflow as tf
import os


def syn():
    """模拟同步读取数据"""
    # 定义队列
    queue = tf.FIFOQueue(3, tf.float32)

    # 放入数据
    ena_many = queue.enqueue_many([[0.1, 0.2, 0.3], ])

    # 定义一些处理数据的逻辑：取数据，+1，入队列
    out_q = queue.dequeue()
    out_q += 1
    en_q = queue.enqueue(out_q)

    with tf.Session() as sess:
        # 初始化队列
        sess.run(ena_many)

        # 处理数据
        for i in range(100):
            sess.run(en_q)

        # 训练数据
        for i in range(queue.size().eval()):
            print(sess.run(queue.dequeue()))


def async():
    """模拟异步读取数据"""
    # 定义一个队列
    queue = tf.FIFOQueue(1000, tf.float32)

    # 模拟处理数据：循环自增，放入队列
    var = tf.Variable(0.0)

    # 实现一个自增，tf.assign_add
    data = tf.assign_add(var, tf.constant(1.0))
    en_q = queue.enqueue(data)

    # 定义队列管理器op，指定多少个子线程，子线程任务
    qr = tf.train.QueueRunner(queue, enqueue_ops=[en_q] * 2)

    # 初始化变量的op
    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 开启线程管理器
        coord = tf.train.Coordinator()

        # 真正开启子线程,start=True：子线程默认启动
        threads = qr.create_threads(sess, coord=coord, start=True)

        # 主线程，不断读取数据训练
        for i in range(300):
            print(sess.run(queue.dequeue()))

        # 回收子线程
        coord.request_stop()
        coord.join(threads)


def csv_read(file_list):
    """读取csv文件"""
    # 构造文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 构造csv阅读器队列数据（按行）
    reader = tf.TextLineReader()
    key, value = reader.read(file_queue)

    # 对每行内容解码，返回列
    # record_defaults：指定每个样本的每一列类型；指定缺失默认值
    records = [["None"], ["None"]]
    example, label = tf.decode_csv(value, record_defaults=records)

    # 批处理，batch_size大小跟队列、数据的数量没有影响，只决定每批取多少数据
    # capacity一般和batch_size取相等
    example_batch, label_batch = tf.train.batch([example, label], batch_size=9, num_threads=1, capacity=9)
    return example_batch, label_batch


def csv_main():
    # 构建文件列表
    file_name = os.listdir("./csvdata")
    file_list = [os.path.join("./csvdata", file) for file in file_name]
    # 接收文件内容
    example_batch, label_batch = csv_read(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()

        # 开启读文件的线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取的内容
        print(sess.run([example_batch, label_batch]))

        # 回收子线程
        coord.request_stop()
        coord.join(threads)


def pic_read(file_list):
    # 构造文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 构造阅读器去读取图片内容（默认读取一张图片）
    reader = tf.WholeFileReader()
    key, value = reader.read(file_queue)

    # 对读取的图片数据进行解码
    image = tf.image.decode_jpeg(value)

    # 处理图片的大小（统一大小）
    image_resize = tf.image.resize_images(image, [200, 200])

    # 在批处理时候需要样本的形状是固定的
    image_resize.set_shape([200, 200, 3])

    # 批处理
    image_batch = tf.train.batch([image_resize], batch_size=20, num_threads=1, capacity=20)

    return image_batch


def pic_main():
    # 构建文件列表
    file_name = os.listdir("./dog")
    file_list = [os.path.join("./dog", file) for file in file_name]
    # 接收文件内容
    image_batch = pic_read(file_list)

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()

        # 开启读文件的线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 打印读取的内容
        print(sess.run([image_batch]))

        # 回收子线程
        coord.request_stop()
        coord.join(threads)


# 定义cifar的数据等命令行参数
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("cifar_dir", "./cifar10/cifar-10-batches-bin/", "文件的目录")
tf.app.flags.DEFINE_string("cifar_tfrecords", "./cifar.tfrecords", "存进tfrecords的文件")


class CifarRead(object):
    def __init__(self, file_list):
        self.file_list = file_list

        # 定义读取的图片的属性
        self.height, self.width, self.channel = 32, 32, 3
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.image_bytes + self.label_bytes

    def read_and_decode(self):
        file_queue = tf.train.string_input_producer(self.file_list)

        reader = tf.FixedLengthRecordReader(self.bytes)
        key, value = reader.read(file_queue)

        # 二进制解码
        label_image = tf.decode_raw(value, tf.uint8)

        # 分割出图片和标签，特征值和目标值
        label = tf.cast(tf.slice(label_image, [0], [self.label_bytes]), tf.int32)
        image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])

        # 对图片的特征数据进行形状改变
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])

        # 批处理
        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=10, num_threads=1, capacity=10)

        return image_batch, label_image

    def write_to_tfrecords(self):
        """将二进制数据写入tfrecords格式"""
        # 建立TFRecord存储器
        writer = tf.python_io.TFRecordWriter(FLAGS.cifar_tfrecords)

        # 循环将所有样本写入文件，每张图片样本都要构造example协议
        image_batch, label_batch = self.read_and_decode()
        for i in range(10):
            image = image_batch[i].eval().tostring()
            label = label_batch[i].eval()[0]

            # 构造一个样本的example
            example = tf.train.Example(features=tf.train.Features(feature={
                "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
            }))

            # 写入单独的样本
            writer.write(example.SerializeToString())

        writer.close()

    def read_from_tfrecords(self):
        file_queue = tf.train.string_input_producer([FLAGS.cifar_tfrecords])

        reader = tf.TFRecordReader()
        key, value = reader.read(file_queue)

        # 解析example
        features = tf.parse_single_example(value, features={
            "images": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.int64),
        })

        # 解码内容，如果读取的内容格式是string则需要解码，如果是int64,float32不需要
        image = tf.decode_raw(features["image"], tf.uint8)
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        label = tf.cast(features["label"], tf.int32)

        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=10, num_threads=1, capacity=10)

        return image_batch, label_batch


def bin_main():
    # 构建文件列表
    file_name = os.listdir(FLAGS.cifar_dir)
    file_list = [os.path.join(FLAGS.cifar_dir, file) for file in file_name]

    # 开启会话运行结果
    with tf.Session() as sess:
        # 定义一个线程协调器
        coord = tf.train.Coordinator()

        # 开启读文件的线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 存进tfrecords文件
        cr = CifarRead(file_list)
        cr.write_to_tfrecords()

        # 从tfrecords文件读取数据
        cr.read_from_tfrecords()

        # 回收子线程
        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    # syn()
    # async()
    csv_main()
