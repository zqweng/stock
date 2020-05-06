#!/usr/bin/python3
# -*- coding: utf-8 -*-
import driver5 as dr5
from datetime import datetime
import stock_library2 as lib2
import pdb
import plot

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


def counting_break_upper_band_after_n(offset=0, num = 8, type='day',  df1=None):
    lib2.head_offset = offset
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "upper", 0.007), cross_type="binary-cmp",
                             period_type=type, rank=True)

    for i in range(1, num):
        lib2.head_offset = i + offset
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("upper", "close"), cross_type="binary-cmp",
                                 period_type=type)

    print(df1.index.to_list())
    plot.plot_stock_list(df1.index.to_list())

    str_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_close_above_upper_" + type + '-' + str_time + '_offset_' + str(offset) + '_days_' + str(num) + ".csv")
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


"""
lib2.head_offset = 0
df = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(4, 10), period_type='day')
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp")
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("upper", "close"), cross_type="binary-cmp",
                          rank=True)

plot.plot_stock_list(df.index.to_list())

lib2.head_offset = 7
df1 = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                          rank=True)
df1.to_csv(r"result/n-{}.csv".format(lib2.head_offset))
lib2.head_offset = 6
df2 = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                          rank=True)
"""

#df1 = counting_break_upper_band_after_n(offset=0)
#df1 = counting_ma20_go_up()
#print(df1)
weeks_up_above_40p()
