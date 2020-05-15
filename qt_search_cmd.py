#!/usr/bin/python3
# -*- coding: utf-8 -*-
import driver5 as dr5
from datetime import datetime
import stock_library2 as lib2
import pdb
import plot
import pandas as pd
import os
import tushare as ts
from load_from_baostock import *

def weeks_up_above_40p():
    df1 = None
    lib2.head_offset = 2
    df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(40, 1100), period_type='week')
    print(df1.index.to_list())
    plot.plot_stock_list(df1.index.to_list())

    lib2.head_offset = 3
    df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(40, 1100), period_type='week')
    print(df1.index.to_list())
    plot.plot_stock_list(df1.index.to_list())


def counting_break_upper_band_after_n(signal, start_offset=0, end_offset=0, num = 8, type='day',  df1=None):
    df1 = pd.DataFrame()
    for offset in range(start_offset, end_offset + 1):
        signal.emit("start offset {}".format(offset))
        lib2.head_offset = offset
        df1 = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "upper", 0.007), cross_type="binary-cmp",
                             period_type=type, rank=True)
        for i in range(1, num):
            lib2.head_offset = i + offset
            df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("upper", "close"), cross_type="binary-cmp",
                                 period_type=type)

    if not df1.empty:
        print(df1.index.to_list())

    return df1


def counting_ma20_go_up():
    df = dr5.get_a_across_b(period_of_days=120, cross_above="ma20", cross_type="unary-current-trend",
                             period_type='day')

    df_pos = df[df['p1'] > 3]
    df_pos = df_pos.sort_values("p1", ascending=False)
    df_pos = dr5.get_a_across_b(df_pos, period_of_days=120, cross_above="ma10", cross_type="unary-current-trend",
                            period_type='day')

    df_pos = df_pos[df_pos['p1'] > 2]
    df_pos = dr5.get_a_across_b(df_pos, period_of_days=120, cross_above="ma5", cross_type="unary-current-trend",
                            period_type='day')

    df_pos = df_pos[df_pos['p1'] > 0]

    pdb.set_trace()
    str_time = datetime.now().strftime("%Y-n%m-%d-%H-%M-%S")
    df_pos.to_csv("current_trend_pos_" + str_time + '.csv')
    return df1


def update_stock_list():
    os.system('cp basic-no3.csv basic-no3-old.csv')

    df = ts.get_stock_basics()

    df = df[df.index.str.startswith("3") == False]
    df = df[df.index.str.startswith("68") == False]
    df = df.sort_index()

    df.to_csv("basic-no3.csv")

def download_30min():
    tick_dir = r'/home/johnny/stockdata-bao'
    ticker_list = r'/home/johnny/code/stock/basic-no3.csv'
    load_history_min(tick_dir, ticker_list, ktype_val="30")

def search_func(cmd_list):
    df1 = pd.DataFrame()
    for cmd_dic in cmd_list:
        duration = cmd_dic["end_offset"] - cmd_dic["start_offset"]
        if duration < 0:
            print("invalid offset")
            continue

        lib2.head_offset = cmd_dic["start_offset"]

        for k, v in cmd_dic.items():
            print(k,v)

        item2 = cmd_dic["cross_over"][1]
        if df1.empty:
            if "%" in item2:
                percent = float(item2[:-1])
                df1 = dr5.get_price_up_with_percentage(period_of_days=duration + 1,
                                                       p_change=(percent, 11),
                                                       period_type=cmd_dic["period_type"])
            else:
                df1 = dr5.get_a_across_b(period_of_days=duration + 1,
                                         cross_above=cmd_dic["cross_over"],
                                         cross_type="binary-cmp",
                                         period_type=cmd_dic["period_type"])
        else:
            if "%" in item2:
                percent = float(item2[:-1])
                df1 = dr5.get_price_up_with_percentage(period_of_days=duration + 1,
                                                       p_change=(percent, 11),
                                                       period_type=cmd_dic["period_type"])
            else:
                df1 = dr5.get_a_across_b(df1,
                                         period_of_days=duration + 1,
                                         cross_above=cmd_dic["cross_over"],
                                         cross_type="binary-cmp",
                                         period_type=cmd_dic["period_type"])

        print(df1)

    df1.to_csv("search.csv")

def add_price_for_monitor():
    df = pd.read_csv("search.csv", converters={"code": lambda x: str(x)})
    df["monitor"] = 0.0

    for row in df.itertuples():
        datafile = pd.read_csv("/home/johnny/stockdata-bao/30/{}.csv".format(row.code))
        df.at[row.Index, "monitor"] = round(datafile.head(1).upper, 2)

    df.to_csv("monitor.csv")

if __name__ == "__main__":
    add_price_for_monitor()