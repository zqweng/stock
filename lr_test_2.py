import pandas as pd
from io import StringIO
from os import path
import numpy as np

from sklearn import linear_model, preprocessing

import matplotlib.pyplot as plt

import pdb
import plot
import os


def load_data(row, df_result=None, period = 10, step = 5, period_type = 'day'):
    file = "/home/johnny/stockdata-bao/{}/{}.csv".format(period_type,row.code)
    if not os.path.isfile(file):
        print("{} not exist".format(file))
        return

    step = step


    df = pd.read_csv(file, nrows= period)
    df = df.sort_index(ascending=False)
    df = df.reset_index()
    data = df["upper"]

    if np.isnan(data).any():
        return

    for i in range(len(data) - step + 1):
        train_y = data.values[i:i+step]
        x = np.arange(step)
        train_x = x.reshape(-1, 1)

        #print(train_y)

        # 建立线性回归模型
        regr = linear_model.LinearRegression()

        # 拟合
        regr.fit(train_x, train_y)  # 注意此处.reshape(-1, 1)，因为X是一维的！

        # 不难得到直线的斜率、截距
        a, b = regr.coef_, regr.intercept_

        a = 17 * a / train_y[0]

        #print(a, b)

        predict = regr.predict(train_x)
        diff_abs = np.absolute(train_y - predict)
        vmr = np.sum(diff_abs)/np.mean(train_y)

        df_tmp = df[i:i+step].reset_index()
        df_tmp["predict"] = predict

        #print("vmr {}".format(vmr))
        if a > 0.5 and vmr < 0.05:
            print(" {} coef {}  vmr {} ".format(row.code, a, vmr))
            if df_result != None:
                df_result.loc[len(df_result.index)] = [row.code, row.name, df_tmp["date"][0], vmr, a, b]
                filename = "{}_1".format(str(len(df_result.index)))
            else:
                filename = row.code
            plot.plot_simple(df_tmp, filename, subtitle ="code = {} vmr={} coef={} inter={}".format(row.code, vmr, a, b))

        if df_result == None:
            plot.plot_simple(df_tmp, subtitle="code = {} vmr={} coef={} inter={}".format(row.code, vmr, a, b))

    return df_tmp


def load_data2(row, df_result=None, period = 10, step = 5, period_type = 'day'):
    file = "/home/johnny/stockdata-bao/{}/{}.csv".format(period_type,row.code)
    if not os.path.isfile(file):
        print("{} not exist".format(file))
        return

    step = step


    df = pd.read_csv(file, nrows= period)

    df = df.drop(columns="date")
    df = df.sort_index(ascending=False)
    df = df.reset_index()
    data = df["upper"]

    if np.isnan(data).any():
        return

    for i in range(len(data) - step + 1):

        train_y = data.values[i:i+step]
        min_y = min(train_y)
        train_y = train_y/min_y

        x = np.arange(step)
        train_x = x.reshape(-1, 1)

        #print(train_y)

        # 建立线性回归模型
        regr = linear_model.LinearRegression()

        # 拟合
        regr.fit(train_x, train_y)  # 注意此处.reshape(-1, 1)，因为X是一维的！

        # 不难得到直线的斜率、截距
        a, b = regr.coef_, regr.intercept_

        a = 17 * a / train_y[0]

        #print(a, b)

        predict = regr.predict(train_x)
        diff_abs = np.absolute(train_y - predict)
        vmr = np.sum(diff_abs)/np.mean(train_y)

        df_tmp = df[i:i+step].reset_index()
        df_tmp = df_tmp/min_y

        df_tmp["predict"] = predict

        #print("vmr {}".format(vmr))
        #if a > 0.0 and vmr < 0.1:
        if 1:
            print(" {} coef {}  vmr {} ".format(row.code, a, vmr))
            if df_result is not None:
                df_result.loc[len(df_result.index)] = [row.code, row.name, vmr, a, b]
                filename = "{}_{}_1".format(row.code, str(len(df_result.index)))
            else:
                filename = "{}_{}_1".format(row.code, i)
            plot.plot_simple(df_tmp, filename, subtitle ="code = {} vmr={} coef={} inter={}".format(row.code, vmr, a, b))

        #if df_result is None:
        #    plot.plot_simple(df_tmp, subtitle="code = {} vmr={} coef={} inter={}".format(row.code, vmr, a, b))

    return df_tmp


def check_slope(df=None, period_type="day", period = 10):

    df_result = pd.DataFrame(columns=["code", "name", "vmr", "coef", "intercept"])
    df_result.vmr = df_result.vmr.astype("float32")
    df_result.coef = df_result.coef.astype("float32")
    df_result.intercept = df_result.intercept.astype("float32")

    if df is None:
        df = pd.read_csv("basic-no3.csv", converters={"code": lambda x: str(x)})

    for row in df.itertuples():
        load_data2(row, df_result, period=period, period_type=period_type)

    return df_result

def get_unique_df(df):
    df_new = pd.DataFrame(columns=["code", "name"])
    for row in df.itertuples():
        if not row.code in df_new["code"].values:
            df_new.loc[len(df_new.index)] = [row.code, row.name]

    return df_new

#df = pd.read_csv("search.csv", converters={"code": lambda x: str(x)})
#df = check_slope(period_type="day", period=10)
#df.to_csv("check_slope.csv")

#df = get_unique_df(df)
#df.to_csv("check_slope_search.csv")
os.system('rm pic/* -f')
se = pd.Series({"code":"002351", "name":"大连重工"})
load_data2(se, period=20, period_type = 'day')
