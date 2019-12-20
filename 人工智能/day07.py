import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("job_name", "", "启动服务的类型ps or worker")
tf.app.flags.DEFINE_integer("task_index", 0, "指定ps或worker中哪一台服务器task:0,task:1")


def main(argv):
    # 定义全局计数的op,给钩子列表中的训练步数使用
    global_step = tf.contrib.framework.get_or_create_global_step()

    # 指定集群描述对象，ps,worker
    cluster = tf.train.ClusterSpec({"ps": ["192.168.16.118:2223"], "worker": ["192.168.16.118:2222"]})

    # 创建不同的服务，ps,worker
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

    # 根据不同服务做不同的事情 ps:去更新保存参数 worker：指定设备区运行模型
    if FLAGS.job_name == "ps":
        server.join()
    else:
        worker_device = "/job:worker/task:0/cpu:0/"

        # 可以指定设备运行
        with tf.device(tf.train.replica_device_setter(
            worker_device=worker_device,
            cluster=cluster
        )):
            # 简单做一个矩阵运算
            x = tf.Variable([[1, 2, 3, 4]])
            w = tf.Variable([[1], [2], [3], [4]])
            mat = tf.matmul(x, w)

        # 创建分布式会话
        with tf.train.MonitoredTrainingSession(
            master="grpc://192.168.16.118:2222",  # 指定主worker
            is_chief=(FLAGS.task_index == 0),  # 判断是否是主worker
            config=tf.ConfigProto(log_device_placement=True),  # 打印设备信息
            hooks=[tf.train.StopAtStepHook(last_step=200)]
        ) as mon_sess:
            while not mon_sess.should_stop():
                mon_sess.run(mat)


if __name__ == '__main__':
    tf.app.run()
