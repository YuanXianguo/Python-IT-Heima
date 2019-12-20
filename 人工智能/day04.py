import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def graph_():
    g = tf.Graph()
    print(g)
    with g.as_default():
        c = tf.constant(11.0)
        print(c.graph)

    a = tf.constant(5.0)
    b = tf.constant(6.0)

    sum1 = tf.add(a, b)

    # 默认的这张图，相当于是给程序分配一段内存
    graph = tf.get_default_graph()
    print(graph)

    # 实时的提供数据去进行训练
    # placeholder是一个占位符，feed_dict是一个字典
    plt = tf.placeholder(tf.float32, [None, 3])
    print(plt)

    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
        print(sess.run(plt, feed_dict={plt: [[1, 2, 3], [4, 5, 6]]}))
        print(sess.run(sum1))
        print(sum1.eval())
        print(sess.graph)
        print(a.graph)
        print(sum1.graph)


def tensor_():
    # 对于静态形状，一旦张量形状固定，不能再次设置
    plt = tf.placeholder(tf.float32, [None, 2])
    print(plt)

    plt.set_shape([3, 2])
    print(plt)

    # plt.set_shape([2, 3])  # 不能再次设置

    # 动态形状可以创建一个新的张量
    plt_reshape = tf.reshape(plt, [2, 3])
    print(plt_reshape)

    # plt_reshape = tf.reshape(plt, [3, 3])  # 元素数量需要一致


def variable():
    a = tf.constant(4.0, name="a")
    b = tf.constant(5.0, name="b")
    c = tf.add(a, b, name="c")

    # 变量op
    var = tf.Variable(tf.random_normal([2, 3], mean=0.0, stddev=1.0), name="var")
    print(a, var)

    # 必须显示的初始化op
    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:
        # 必须运行初始化op
        sess.run(init_op)

        # 把程序的图结构写入事件文件
        filewriter = tf.summary.FileWriter("./summary/test", graph=sess.graph)

        print(sess.run([c, var]))


tf.app.flags.DEFINE_integer("max_step", 100, "最大训练步数")
tf.app.flags.DEFINE_string("model_dir", "./ckpt/myre_model", "模型路径")
FLAGS = tf.app.flags.FLAGS


def my_regression():
    """自定义线性回归"""
    with tf.variable_scope("data"):
        # 1、准备数据，实际应用中，特征值和目标值都是读取的，这里自定义
        # x特征值[100,1]
        x = tf.random_normal([100, 1], mean=1.75, stddev=0.5, name="x_data")
        # y目标值[100]，矩阵相乘必须是二维的
        y_true = tf.matmul(x, [[0.7]]) + 0.8

    with tf.variable_scope("model"):
        # 2、建立线性回归模型，1个特征，1个权重，1个偏置 y = x w + b
        # 随机给一个权重和偏置的值，然后计算损失，在当前状态下优化
        # 模型用变量定义才能优化
        weight = tf.Variable(tf.random_normal([1, 1], mean=0.0, stddev=1.0, name='w'))
        bias = tf.Variable(0.0, name='b')

        # 预测目标值
        y_predict = tf.matmul(x, weight) + bias

    with tf.variable_scope("loss"):
        # 3、建立损失函数，均方误差
        loss = tf.reduce_mean(tf.square(y_true - y_predict))

    with tf.variable_scope("optimizer"):
        # 4、梯度下降优化损失，learning_rate：0-1，2，3，5，7，10
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 收集tensor，一般在会话前
    tf.summary.scalar("losses", loss)
    tf.summary.histogram("weights", weight)

    # 合并tensor
    merged = tf.summary.merge_all()

    # 定义一个初始化的op
    init_op = tf.global_variables_initializer()

    # 定义一个保存模型的实例
    saver = tf.train.Saver()

    # 通过会话运行程序
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 打印随机初始化的权重和偏置
        print("随机初始化的参数权重为：{}，偏置为：{}".format(weight.eval(), bias.eval()))

        # 建立事件文件
        file_writer = tf.summary.FileWriter("./summary/test", graph=sess.graph)

        # 加载模型，从上次训练的参数结果开始
        if os.path.exists(FLAGS.model_dir):
            saver.restore(sess, FLAGS.model_dir)

        # 循环训练，运行优化
        for i in range(FLAGS.max_step):
            sess.run(train_op)

            # 运行合并的tensor
            summary = sess.run(merged)

            file_writer.add_summary(summary, i)

            print("第{}次，参数权重为：{}，偏置为：{}".format(i, weight.eval(), bias.eval()))
            saver.save(sess, FLAGS.model_dir)


if __name__ == '__main__':
    # tensor_()
    # variable()
    # "./ckpt/model"
    my_regression()
