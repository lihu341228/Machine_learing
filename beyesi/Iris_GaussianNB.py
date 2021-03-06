#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
#所有评估的指标，都在metrics里面
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


if __name__ == "__main__":
    # 使用pandas来读数据，header=None意味着你的数据第一行上来就是数据本身
    data = pd.read_csv('./iris.data', header=None)
    # 取数据集里面0，1，2，3列数据赋给x,data[4]取类别名称赋值y
    x, y = data[np.arange(4)], data[4]
    # 把类别字符串转成从0开始的类别号
    y = pd.Categorical(values=y).codes

    feature_names = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'
    features = [0,1]
    # 取u'花萼长度', u'花萼宽度'两列数据
    x = x[features]
    # 训练集占用70%，测试集30%，random_state是随机种子
    # 随机种子如果赋值给写死了，每次执行测试集和训练集分开的数据是一样的
    x, x_test, y, y_test = train_test_split(x, y, train_size=0.7, random_state=0)

    # 下面两行做的事情就是为了后面给算法穿超参准备数据，GaussianNB(priors=priors)
    priors = np.array((1, 1, 1), dtype=float)
    priors /= priors.sum()
    # Pipeline是sklearn里面的一个封装的类，作用可以一下按照设定的顺序取执行
    gnb = Pipeline([
        # StandardScaler默认是做均值归一化、方差归一化
        ('sc', StandardScaler()),
        # 相当于对数据进行升维，Note:它会自动添加X0
        ('poly', PolynomialFeatures(degree=2)),
        # priors指定与否取决与你的数据集类别样本数据量是否均衡，如果不均衡需要指定一下
        ('clf', GaussianNB(priors=priors))])    # 由于鸢尾花数据是样本均衡的，其实不需要设置先验值
    #因为是连续的，样本数据集，所以选用高沙贝叶斯。
    # gnb = KNeighborsClassifier(n_neighbors=3).fit(x, y.ravel())
    gnb.fit(x, y.ravel())
    y_hat = gnb.predict(x)
    print('训练集准确度: %.2f%%' % (100 * accuracy_score(y, y_hat)))
    y_test_hat = gnb.predict(x_test)
    print('测试集准确度：%.2f%%' % (100 * accuracy_score(y_test, y_test_hat)))  # 画图

    N, M = 500, 500     # 横纵各采样多少个值
    x1_min, x2_min = x.min()
    x1_max, x2_max = x.max()
    t1 = np.linspace(x1_min, x1_max, N)
    t2 = np.linspace(x2_min, x2_max, M)
    x1, x2 = np.meshgrid(t1, t2)                    # 生成网格采样点
    x_grid = np.stack((x1.flat, x2.flat), axis=1)   # 测试点

    mpl.rcParams['font.sans-serif'] = [u'simHei']
    mpl.rcParams['axes.unicode_minus'] = False
    cm_light = mpl.colors.ListedColormap(['#77E0A0', '#FF8080', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    y_grid_hat = gnb.predict(x_grid)                  # 预测值
    y_grid_hat = y_grid_hat.reshape(x1.shape)
    plt.figure(facecolor='w')
    plt.pcolormesh(x1, x2, y_grid_hat, cmap=cm_light)     # 预测值的显示
    plt.scatter(x[features[0]], x[features[1]], c=y, edgecolors='k', s=50, cmap=cm_dark)
    plt.scatter(x_test[features[0]], x_test[features[1]], c=y_test, marker='^', edgecolors='k', s=120, cmap=cm_dark)

    plt.xlabel(feature_names[features[0]], fontsize=13)
    plt.ylabel(feature_names[features[1]], fontsize=13)
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.title(u'GaussianNB对鸢尾花数据的分类结果', fontsize=18)
    plt.grid(True)
    plt.show()

