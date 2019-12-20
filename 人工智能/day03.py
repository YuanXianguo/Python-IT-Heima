from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.externals import joblib
import pandas as pd
import numpy as np


def my_linear():
    """线性回归直接预测房子价格"""

    # 获取数据
    lb = load_boston()

    # 分割数据集
    train_x, test_x, train_y, test_y = train_test_split(lb.data, lb.target, test_size=0.25)

    # 进行标准化处理，特征值和目标值都必须标准化处理，实例化两个标准API
    std_x = StandardScaler()
    train_x = std_x.fit_transform(train_x)
    test_x = std_x.transform(test_x)

    std_y = StandardScaler()
    train_y = std_y.fit_transform(train_y.reshape(-1, 1))
    test_y = std_y.transform(test_y.reshape(-1, 1))

    # 正规方程求解方式预测结果
    lr = LinearRegression()
    lr.fit(train_x, train_y)
    print("回归系数：\n", lr.coef_)

    # 保存训练好的模型
    joblib.dump(lr, "test.pkl")

    # 加载保存模型
    lr = joblib.load("test.pkl")

    # 预测测试集的房子价格
    predict_y_lr = std_y.inverse_transform(lr.predict(test_x))
    print("测试集里每个房子预测价格：\n", predict_y_lr)
    mean_error_lr = mean_squared_error(std_y.inverse_transform(test_y), predict_y_lr)
    print("正规方程的均方误差：", mean_error_lr)

    # 梯度下降预测结果
    sgd = SGDRegressor()
    sgd.fit(train_x, train_y)
    print("回归系数：\n", sgd.coef_)

    predict_y_sgd = std_y.inverse_transform(sgd.predict(test_x))
    print("测试集里每个房子预测价格：\n", predict_y_sgd)
    mean_error_sgd = mean_squared_error(std_y.inverse_transform(test_y), predict_y_sgd)
    print("梯度下降均方误差：", mean_error_sgd)

    # 岭回归预测房价
    rd = Ridge(alpha=1.0)
    rd.fit(train_x, train_y)
    print("回归系数：\n", rd.coef_)

    predict_y_rd = std_y.inverse_transform(rd.predict(test_x))
    print("测试集里每个房子预测价格：\n", predict_y_rd)
    mean_error_rd = mean_squared_error(std_y.inverse_transform(test_y), predict_y_rd)
    print("岭回归均方误差：\n", mean_error_rd)


def logistic():
    """逻辑回归做二分类进行癌症预测（根据细胞的属性特征）"""

    # 构造列标签名字
    column = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size',
              'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size',
              'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

    # 读取数据
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/" \
          "breast-cancer-wisconsin/breast-cancer-wisconsin.data"
    data = pd.read_csv(url, names=column)

    # 缺失值处理
    data = data.replace(to_replace="?", value=np.nan)
    data = data.dropna()

    # 进行数据的分割
    train_x, test_x, train_y, test_y = train_test_split(data[column[1:10]], data[column[10]], test_size=0.25)

    # 标准化处理
    std = StandardScaler()
    train_x = std.fit_transform(train_x)
    test_x = std.transform(test_x)

    # 逻辑回归预测
    lg = LogisticRegression(C=1.0)
    lg.fit(train_x, train_y)
    print("回归系数：\n", lg.coef_)
    print("准确率：", lg.score(test_x, test_y))
    predict_y = lg.predict(test_x)
    print("召回率：\n", classification_report(test_y, predict_y, labels=[2, 4], target_names=["良性", "恶行"]))


if __name__ == '__main__':
    # my_linear()
    logistic()
