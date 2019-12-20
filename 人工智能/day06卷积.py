import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


class ConvFc(object):
    def weight_var(self, shape):
        w = tf.Variable(tf.random_normal(shape=shape, mean=0.0, stddev=1.0))
        return w

    def bias_var(self, shape):
        b = tf.Variable(tf.constant(0.0, shape=shape))
        return b

    def model(self):
        """自定义卷积模型"""
        with tf.variable_scope("data"):
            x = tf.placeholder(tf.float32, [None, 784])
            y_true = tf.placeholder(tf.int32, [None, 10])

        # 卷积层一，卷积：5*5*1，32个，strides=1 激活 池化
        with tf.variable_scope("conv1"):
            # 随机初始化权重，偏置
            w_conv1 = self.weight_var([5, 5, 1, 32])
            b_conv1 = self.bias_var([32])

            # 对x进行形状的改变[None, 784] --> [None, 28, 28, 1]
            x_reshape = tf.reshape(x, [-1, 28, 28, 1])

            # 卷积[None, 28, 28, 1] --> [None, 28, 28, 32]
            conv = tf.nn.conv2d(x_reshape, w_conv1, strides=[1, 1, 1, 1], padding="SAME") + b_conv1

            x_relu1 = tf.nn.relu(conv)  # 激活

            # 池化 2*2，strides=2 [None, 28, 28, 32][None, 14, 14, 32]
            x_pool1 = tf.nn.max_pool(x_relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

        # 卷积层二 卷积：5*5*32，64个filter，strides=1 激活 池化
        with tf.variable_scope("conv2"):
            w_conv2 = self.weight_var([5, 5, 32, 64])
            b_conv2 = self.bias_var([64])

            # [None, 14, 14, 32] --> [None, 14, 14, 64]
            conv2 = tf.nn.conv2d(x_pool1, w_conv2, strides=[1, 1, 1, 1], padding="SAME") + b_conv2
            x_relu2 = tf.nn.relu(conv2)
            x_pool2 = tf.nn.max_pool(x_relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

        # 全连接层 [None, 7, 7, 64] --> [None, 7 * 7 * 64] * [7 * 7 * 64, 10] + [10] = [None, 10]
        w_fc = self.weight_var([7 * 7 * 64, 10])
        b_fc = self.bias_var([10])

        x_fc_reshape = tf.reshape(x_pool2, [-1, 7 * 7 * 64])

        y_predict = tf.matmul(x_fc_reshape, w_fc) + b_fc

        return x, y_true, y_predict

    def main(self):
        mnist = input_data.read_data_sets("./mnist/input_data", one_hot=True)

        # 定义模型，得出输出
        x, y_true, y_predict = self.model()

        # 求平均交叉熵
        with tf.variable_scope("soft_cross"):
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

        # 梯度下降求出损失
        with tf.variable_scope("optimizer"):
            train_op = tf.train.GradientDescentOptimizer(0.0001).minimize(loss)

        # 计算准确率
        with tf.variable_scope("acc"):
            equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
            accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

        init_op = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init_op)
            for i in range(1000):
                mnist_x, mnist_y = mnist.train.next_batch(50)
                sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})
                print("执行{}步，准确率为：{}".format(i, sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y})))


if __name__ == '__main__':
    conv_fc = ConvFc()
    conv_fc.main()
