from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def iris_predict():
    # 鸢尾花数据集
    iris = load_iris()

    print("特征值：{}；目标值：{}，描述：{}".format(iris.data, iris.target, iris.DESCR))

    # 返回值分别为，训练集特征值，目标值和测试集特征值，目标值
    train_x, test_x, train_y, test_y = train_test_split(iris.data, iris.target, test_size=0.25)

    print("训练集特征值和目标值：{}，{}".format(train_x, train_y))
    print("测试集特征值和目标值：{}，\n{}".format(test_x, test_y))

    # 标准化
    std = StandardScaler()
    std.fit_transform(train_x)
    std.transform(test_x)

    # 评估
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(train_x, train_y)
    predict = knn.predict(test_x)
    score = knn.score(test_x, test_y)

    print("预测特征值：{}，\n预测准确率：{}".format(predict, score))


def knncls():
    """k近邻算法"""
    # 1.读取数据
    data = pd.read_csv("train.csv")

    # 2.处理数据
    # 缩小数据，查询数据筛选
    data = data.query("x > 1.0 & x < 1.25 & y > 2.5 & y < 2.75")

    # 处理时间的数据
    time_value = pd.to_datetime(data['time'], unit='s')

    # 把日期格式转换成字典格式
    time_value = pd.DatetimeIndex(time_value)

    # 构造一些特征
    data['day'] = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday

    # 把时间戳和'row_id'特征删除,pandas行0，列1
    data = data.drop(['time'], axis=1)
    data = data.drop(['row_id'], axis=1)

    # 将签到位置少于n个用户的目标位置删除，reset_index将索引置为新列
    place_count = data.groupby('place_id').count()
    tf = place_count[place_count.row_id > 3].reset_index()
    data = data[data['place_id'].isin(tf.place_id)]

    # 取出数据当作的特征值和目标值
    y = data['place_id']
    x = data.drop(['place_id'], axis=1)

    # 进行数据的分割训练集和测试集
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25)

    # 3.特征工程（标准化）
    std = StandardScaler()

    # 对测试集和训练集的特征值进行标准化
    train_x = std.fit_transform(train_x)

    test_x = std.transform(test_x)

    # 4.estimator流程进行分类预测
    knn = KNeighborsClassifier()

    # knn.fit(train_x, train_y)
    #
    # # 得出预测结果
    # predict_y = knn.predict(test_x)
    #
    # # 评估准确率
    # score = knn.score(test_x, test_y)
    # print("预测目标值：{}\n预测准确率：{}".format(predict_y, score))

    # 构造参数
    param = {"n_neighbors": [3, 5, 10]}

    # 进行网格搜索
    gsc = GridSearchCV(knn, param_grid=param, cv=2)

    gsc.fit(train_x, train_y)

    # 预测准确率
    print("在测试集上预测准确率：", gsc.score(test_x, test_y))

    print("在交叉验证中最好的结果：", gsc.best_score_)

    print("选择最好的模型是：", gsc.best_estimator_)

    print("每个超参数每次交叉验证的结果；", gsc.cv_results_)

    return


def naviebayes():
    """朴素贝叶斯进行文本分类"""
    news = fetch_20newsgroups(subset="all")

    # 进行数据分割
    train_x, test_x, train_y, test_y = train_test_split(news.data, news.target, test_size=0.25)

    # 对数据集进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词的列表进行每篇文章重要性统计
    train_x = tf.fit_transform(train_x)

    test_x = tf.transform(test_x)

    # 进行朴素贝叶斯算法的预测
    mlt = MultinomialNB(alpha=1.0)
    mlt.fit(train_x, train_y)

    predict = mlt.predict(test_x)
    score = mlt.score(test_x, test_y)

    print("预测目标值：{}\n预测准确率：{}".format(predict, score))

    print("每个类别的精确率和召回率：\n", classification_report(test_y, predict, target_names=news.target_names))

    return


def decision():
    """决策树对泰坦尼克号进行生命预测"""
    # 获取数据
    taitan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")
    # 处理特征值和目标值
    x = taitan[['pclass', 'age', 'sex']]
    y = taitan['survived']

    # 缺失值处理，用户平均值填补空值
    x['age'].fillna(x['age'].mean(), inplace=True)

    # 分割数据集
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25)

    # 进行处理（特征工程）特征-》类别-》one_hot编码
    dv = DictVectorizer(sparse=False)

    # train_x.to_dict，pd转换为字典
    train_x = dv.fit_transform(train_x.to_dict(orient="records"))
    test_x = dv.transform(test_x.to_dict(orient="records"))

    # print(dv.get_feature_names())

    # # 用决策树进行预测
    # det = DecisionTreeClassifier()
    # det.fit(train_x, train_y)
    # print("预测准确率：", det.score(test_x, test_y))
    #
    # # 导出决策树的结构
    # names = ['age', 'pclass=1st', 'pclass=2nd', 'pclass=3rd', 'sex=female', 'sex=male']
    # export_graphviz(det, out_file="./tree.dot", feature_names=names)

    # 随机森林进行预测（超参数调优）
    rf = RandomForestClassifier()

    # 网格搜索与交叉验证
    params = {"n_estimators": [120, 200, 300, 500, 800, 1200],
              "max_depth": [5, 8, 15, 25, 30]}
    gsc = GridSearchCV(rf, param_grid=params, cv=2)
    gsc.fit(train_x, train_y)

    print("准确率：", gsc.score(test_x, test_y))
    print("查看选择的参数模型：", gsc.best_params_)


if __name__ == '__main__':
    # iris_predict()
    # naviebayes()
    decision()

