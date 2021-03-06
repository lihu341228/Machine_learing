#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名: music_classifier.py

import numpy as np
from scipy import fft
from scipy.io import wavfile
from sklearn.linear_model import LogisticRegression
import pickle
import pprint

__author__ = 'yasaka'

"""
使用logistic regression处理音乐数据,音乐数据训练样本的获得和使用快速傅里叶变换（FFT）预处理的方法需要事先准备好
1. 把训练集扩大到每类100个首歌,类别是六类:jazz,classical,country, pop, rock, metal
2. 使用logistic回归作为分类器
3. 使用一些新的音乐来测试分类器的准确性
"""


# 准备音乐数据

# def create_fft(g, n):
#     rad = "e:/genres/" + g + "/converted/" + g + "." + str(n).zfill(5) + ".au.wav"
#     (sample_rate, X) = wavfile.read(rad)
#     fft_features = abs(fft(X)[:1000]) #傅里叶变换。
#     sad = "d:/trainset/" + g + "." + str(n).zfill(5) + ".fft"
#     np.save(sad, fft_features)
#
#
# genre_list = ["classical", "jazz", "country", "pop", "rock", "metal"]
# for g in genre_list:
#     for n in range(100):
#         create_fft(g, n) # 将600首歌存储，然后转换存储起来。

# 加载训练集数据,分割训练集以及测试集,进行分类器的训练
# 构造训练集！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# -------read fft--------------
genre_list = ["classical", "jazz", "country", "pop", "rock", "metal"]
X = [] # x1,x2,x3,x4,,x5 是一个二维矩阵
Y = [] # Y 是一个向量
for g in genre_list:
    for n in range(100):
        rad = "e:/StudyMaterials/python/python-sklearn/trainset/" + g + "." + str(n).zfill(5) + ".fft" + ".npy"
        fft_features = np.load(rad) # fft_features  把模型加载出来 是一首音乐的x1,xn的特征。
        X.append(fft_features) # 每次追加一个向量
        Y.append(genre_list.index(g))

X = np.array(X) # sk_learn更多的是需要numpy,pandas这样的数组，所以给转为一维或者二维的数组。
Y = np.array(Y)

# 接下来，我们使用sklearn，来构造和训练我们的分类器
# ------train logistic classifier--------------

model = LogisticRegression() #导入线性模型
model.fit(X, Y) # 默认是解析解

# 可以采用Python内建的持久性模型 pickle 来保存scikit的模型

output = open('data.pkl', 'wb')
pickle.dump(model, output) # pickle存模型
output.close()

pkl_file = open('data.pkl', 'rb')
model_load = pickle.load(pkl_file) # 加载模型
pprint.pprint(model_load) # 打印更加漂亮些
pkl_file.close()


# 测试
print('Starting read wavfile...')
sample_rate, test = wavfile.read("e:/StudyMaterials/python/python-sklearn/trainset/sample/heibao-wudizirong-remix.wav")
testdata_fft_features = abs(fft(test))[:1000] # 傅里叶变换 还是8Kb
print(sample_rate, testdata_fft_features, len(testdata_fft_features))
type_index = model_load.predict([testdata_fft_features])[0]  # 把新的数据加载到模型 返回的是一个集合里面就一个数
print(type_index)
print(genre_list[type_index])
