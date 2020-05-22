import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pdb
import pandas as pd


def plot_nonlinear(x_2data, y_2data):
    # 训练一元线性模型
    model = LinearRegression()
    model.fit(x_2data, y_2data)

    plt.plot(x_2data, y_2data, 'b.')
    plt.plot(x_2data, model.predict(x_2data), 'r')

    # 定义多项式回归：其本质是将变量x，根据degree的值转换为相应的多项式（非线性回归），eg: degree=3,则回归模型
    # 变为 y = theta0 + theta1 * x + theta2 * x^2 + theta3 * x^3
    poly_reg = PolynomialFeatures(degree=3)
    # 特征处理
    x_ploy = poly_reg.fit_transform(x_2data)  # 这个方法实质是把非线性的模型转为线性模型进行处理，
    # 处理方法就是把多项式每项的样本数据根据幂次数计算出相应的样本值(详细理解可以参考我的博文：https://blog.csdn.net/qq_34720818/article/details/103349452)

    # pdb.set_trace()

    # 训练线性模型（其本质是非线性模型，是由非线性模型转换而来）
    lin_reg_model = LinearRegression()
    lin_reg_model.fit(x_ploy, y_2data)

    #plt.plot(x_2data, y_2data, 'b.')
    y_predict = lin_reg_model.predict(x_ploy).round(2)

    print(y_predict[5])
    #pdb.set_trace()
    #plt.plot(x_2data, lin_reg_model.predict(x_ploy), 'r.')
    #for x, y in zip(x_2data, y_predict):
    #    plt.text(x,y, "{}".format(y))

    #plt.show()


file = "/home/johnny/stockdata-bao/day/002351.csv"
df = pd.read_csv(file, nrows=20)
df = df.sort_index(ascending=False)
df = df.reset_index()

y_2data = df["close"].values.reshape(-1, 1)

# 读取数据
x_2data = np.arange(1, len(df.index) + 1).reshape(-1,1)
#y_2data = np.array([45000, 50000, 60000, 80000, 110000, 150000, 200000, 300000, 500000, 1000000]).reshape(-1,1)

#x_2data = x_2data[:-1,]
#y_2data = y_2data[:-1,]
for i in range (8, 0, -1):
    x_2data_tmp = x_2data[:-i,]
    y_2data_tmp = y_2data[:-i,]
    plot_nonlinear(x_2data_tmp, y_2data_tmp)

