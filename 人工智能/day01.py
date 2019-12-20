from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import numpy as np
import jieba


def dictvec():
    """字典特征抽取"""
    # 实例化
    dv = DictVectorizer(sparse=False)

    # 调用fit_transform
    data = dv.fit_transform([{'city': '北京', 'temperature': 100},
                             {'city': '上海', 'temperature': 60},
                             {'city': '深圳', 'temperature': 30}])

    print(dv.get_feature_names())

    print(dv.inverse_transform(data))

    print(data)

    return None


def countvec():
    """文本特征抽取"""

    cv = CountVectorizer()

    data = cv.fit_transform(["life is short,i like python",
                             "life is too long,i dislike python"])

    print(cv.get_feature_names())

    print(data.toarray())

    return None


def get_ch_list():
    s1 = "文本的特征提取应用于很多方面，"
    s2 = "比如说文档分类、垃圾邮件分类和新闻分类。"
    s3 = "那么文本分类是通过词是否存在、以及词的概率（重要性）来表示。"
    contents = list()
    for s in [s1, s2, s3]:
        contents.append(" ".join(list(jieba.cut(s))))
    return contents


def chvec():
    """中文特征抽取"""

    cv = CountVectorizer()

    data = cv.fit_transform(get_ch_list())

    print(cv.get_feature_names())

    print(data.toarray())

    return None


def tfidfvec():
    """tfidf特征抽取"""

    tfidf = TfidfVectorizer()

    data = tfidf.fit_transform(get_ch_list())

    print(tfidf.get_feature_names())

    print(data.toarray())

    return None


def minmax():
    """归一化处理"""
    mm = MinMaxScaler()  # 默认区间[0,1]
    data = mm.fit_transform([[90, 2, 10, 40], [60, 4, 15, 45], [75, 3, 13, 46]])
    print(data)

    return None


def stand():
    """标准化处理"""
    std = StandardScaler()
    data = std.fit_transform([[1., -1., 3.], [2., 4., 2.], [4., 6., -1.]])
    print(data)

    return None


def imputer():
    """缺失值处理"""
    im = Imputer(missing_values="NaN", strategy="mean", axis=0)
    data = im.fit_transform([[1, 2], [np.nan, 3], [7, 6]])
    print(data)

    return None


def variance():
    """特征选择-删除低方差的特征"""
    var = VarianceThreshold(threshold=0.0)
    data = var.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
    print(data)

    return None


def pca():
    """主成分分析"""
    pca = PCA(n_components=0.9)
    data = pca.fit_transform([[2, 8, 4, 5], [6, 3, 0, 8], [5, 4, 9, 1]])
    print(data)

    return None


if __name__ == '__main__':
    # dictvec()
    # countvec()
    # chvec()
    # tfidfvec()
    # minmax()
    # stand()
    # imputer()
    # variance()
    pca()
