import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer("is_train", 1, "指定程序预测或训练")


def full_connect():
    # 获取数据
    mnist = input_data.read_data_sets("./mnist/input_data", one_hot=True)

    # 建立数据的占位符
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 784])
        y_true = tf.placeholder(tf.int32, [None, 10])

    # 建立一个全连接的神经网络
    with tf.variable_scope("fc_model"):
        # 随机初始化权重和偏置
        weight = tf.Variable(tf.random_normal([784, 10]))
        bias = tf.Variable(tf.constant(0.0, shape=[10]))

        # 预测输出结果
        y_predict = tf.matmul(x, weight) + bias

    # 求平均交叉熵损失
    with tf.variable_scope("soft_cross"):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

    # 梯度下降求出损失
    with tf.variable_scope("optimizer"):
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 收集变量
    tf.summary.scalar("losses", loss)
    tf.summary.scalar("acc", accuracy)
    tf.summary.histogram("weights", weight)
    tf.summary.histogram("biases", bias)

    # 合并变量
    merged = tf.summary.merge_all()

    # 创建saver
    saver = tf.train.Saver()

    init_op = tf.global_variables_initializer()

    # 开启会话训练
    with tf.Session() as sess:
        sess.run(init_op)

        # 建立events文件，然后写入
        filewriter = tf.summary.FileWriter("./summary/test", graph=sess.graph)

        if FLAGS.is_train == 1:
            # 迭代更新参数预测
            for i in range(2000):
                # 取出特征值和目标值
                mnist_x, mnist_y = mnist.train.next_batch(50)

                sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

                # 写入每步训练的值
                summary = sess.run(merged, feed_dict={x: mnist_x, y_true: mnist_y})
                filewriter.add_summary(summary, i)

                print("执行{}步，准确率为：{}".format(i, sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y})))

            # 保存模型
            saver.save(sess, "ckpt/fc_model")
        else:
            # 加载模型
            saver.restore(sess, "ckpt/fc_model")
            for i in range(100):
                x_test, y_test = mnist.test.next_batch(1)
                print("第{}张图片，手写数字目标是：{}，预测结果是：{}".format(
                    i,
                    tf.argmax(y_test, 1).eval(),
                    tf.argmax(sess.run(y_predict, feed_dict={x: x_test, y_true: y_test}), 1).eval()
                ))


if __name__ == '__main__':
    full_connect()
