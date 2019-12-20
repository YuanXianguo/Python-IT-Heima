import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("captcha_dir", "./tfrecords/captcha.tfrecords", "验证码数据的路径")
tf.app.flags.DEFINE_integer("batch_size", 100, "每批次训练的样本数")
tf.app.flags.DEFINE_integer("label_num", 4, "每个样本的目标值数量")
tf.app.flags.DEFINE_integer("letter_num", 26, "每个目标值取得字母得可能性个数")


class CaptchaRecognize(object):

    def weight_var(self, shape):
        """定义一个初始化权重的函数"""
        return tf.Variable(tf.random_normal(shape=shape, mean=0.0, stddev=1.0))

    def bias_var(self, shape):
        """定义一个初始化偏置的函数"""
        return tf.Variable(tf.constant(0.0, shape=shape))

    def read_and_decode(self):
        """读取验证码数据API"""
        # 1.构建文件队列
        file_queue = tf.train.string_input_producer([FLAGS.captcha_dir])
        # 2.构建阅读器，读取文件内容，默认一个样本
        reader = tf.TFRecordReader()
        key, value = reader.read(file_queue)

        # 3.tfrecords格式example，需要解析
        features = tf.parse_single_example(value, features={
            "image": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.string)})

        # 4.解码内容，字符串内容，提取出特征值和目标值
        image = tf.decode_raw(features["image"], tf.uint8)
        label = tf.decode_raw(features["label"], tf.uint8)

        # 5.改变形状
        image_reshape = tf.reshape(image, [20, 80, 3])
        label_reshape = tf.reshape(label, [4])
        print(image_reshape, label_reshape)

        # 6.进行批处理，每批次读取的样本数100，也就是每次训练时候的样本
        image_batch, label_batch = tf.train.batch([image_reshape, label_reshape],
                                                  batch_size=FLAGS.batch_size, num_threads=1, capacity=FLAGS.batch_size)
        print(image_batch, label_batch)
        return image_batch, label_batch

    def fc_model(self, image):
        """
        进行结果预测
        :param image: 100张图特征值[100,20,80,3]
        :return: y_predict预测值[100, 4 * 26]
        """
        with tf.variable_scope("model"):
            image_reshape = tf.reshape(image, [-1, 20 * 80 * 3])

            weights = self.weight_var([20 * 80 * 3, 4 * 26])
            bias = self.bias_var([4 * 26])

            # 进行全连接层计算[100, 4 * 26]
            y_predict = tf.matmul(tf.cast(image_reshape, tf.float32), weights) + bias

        print(y_predict)

        return y_predict

    def predict_to_onehot(self, label):
        """将读取文件当中的目标值转换成one-hot编码"""
        label_onehot = tf.one_hot(label, depth=FLAGS.letter_num, on_value=1.0, axis=2)

        print(label_onehot)

        return label_onehot

    def main(self):
        """验证码识别程序"""
        # 1.读取验证码的数据文件 label_batch [100, 4]
        image_batch, label_batch = self.read_and_decode()

        # 2.通过输入图片特征数据，建立模型，得出预测结果
        # matrix [100, 20 * 80 * 3] * [20 * 80 * 3, 4 * 26] + [104] = [100, 4 * 26]
        y_predict = self.fc_model(image_batch)

        # 3.先把目标值转换成one-hot编码 [100,4,26]
        y_true = self.predict_to_onehot(label_batch)

        # 4.softmax计算，交叉熵损失计算
        with tf.variable_scope("soft-cross"):
            # 改变形状 [100, 4, 26] --> [100, 4 * 26]
            label = tf.reshape(y_true, [FLAGS.batch_size, FLAGS.label_num * FLAGS.letter_num])
            # 求平均交叉熵损失
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=label, logits=y_predict))

        # 5.梯度下降优化损失
        with tf.variable_scope("optimizer"):
            train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

        # 6.求出样本的每批次预测的准确率，三维比较
        with tf.variable_scope("acc"):
            y_predict_reshape = tf.reshape(y_predict, [FLAGS.batch_size, FLAGS.label_num, FLAGS.letter_num])
            equal_list = tf.equal(tf.argmax(y_true, 2), tf.argmax(y_predict_reshape, 2))
            accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

        init_op = tf.global_variables_initializer()

        # 开启会话训练
        with tf.Session() as sess:
            sess.run(init_op)

            # 定义线程协调器和开启线程
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess, coord=coord)# 开启线程

            # 训练识别程序
            for i in range(5000):
                sess.run(train_op)
                print("第{}批次的准确率为：{}".format(i, accuracy.eval()))

            # 回收线程
            coord.request_stop()
            coord.join(threads)


if __name__ == '__main__':
    cap_re = CaptchaRecognize()
    cap_re.main()
