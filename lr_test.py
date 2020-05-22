import pandas as pd
from io import StringIO
import numpy as np
import os
from sklearn import linear_model, preprocessing
import matplotlib.pyplot as plt
import pdb
import lr_test_2

mm = preprocessing.MinMaxScaler()

def load_data(row, df_result, period = 10, step = 5, period_type = 'day'):
    file = "/home/johnny/stockdata-bao/{}/{}.csv".format(period_type,row.code)
    if not os.path.isfile(file):
        print("{} not exist".format(file))
        return

    df = pd.read_csv(file, nrows= period)

    data = df["upper"]
    step = step

    print("check {}".format(row.code))

    for i in range(len(data) - step):
        y = data.values[i:i+step]

        # step 1: get the mean value of y
        mean = np.mean(y)

        # step 2: 计算差, 和平方比，没有平方。 variance,  mean(abs(x-mean(x)))
        abs_sum = 0
        for j in y:
            abs_sum += abs(j -mean)
        new_var = abs_sum/len(y)

        # vmr variance to mean ratio
        vmr = 10000 * new_var/mean

        #[17.318 17.324 17.352 17.315 17.303 17.332]
        #0.1352651427691832
        if vmr < 10:
            #print("{}  min_vmr {}".format(code, min_vmr))
            df_result.loc[len(df_result.index)] = [row.code, row.name, df["date"][i]]




def check_zero_slope(df=None, period_type="day", period = 20):

    df_result = pd.DataFrame(columns=["code", "name", "date"])

    if df is None:
        df = pd.read_csv("basic-no3.csv", converters={"code": lambda x: str(x)})

    for row in df.itertuples():
        load_data(row, df_result, period)

    return df_result


#df = pd.read_csv("check_slope_unq.csv", converters={"code": lambda x: str(x)})
df = lr_test_2.check_slope(period_type="day", period=10)
df = lr_test_2.get_unique_df(df)
df = check_zero_slope(df, period=20)
df.to_csv("check_zero_slope_and_climbup.csv")