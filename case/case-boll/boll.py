import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import pdb
import pandas as pd
import datetime

def counting_break_upper_band_after_n(offset=0, num = 8, type='day',  df1=None):
    lib2.head_offset = offset
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("high", "upper"), cross_type="binary-cmp",
                             period_type=type, rank=True)

    for i in range(1, num):
        lib2.head_offset = i + offset
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("upper", "close"), cross_type="binary-cmp",
                                 period_type=type)

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_close_above_upper_" + type + '-' + str_time + '_offset_' + str(offset) + '_days_' + str(num) + ".csv")
    return df1


#counting_break_upper_band_after_n(10, 'day')

#counting_break_upper_band_after_n(20, 'week')
"""
for i in range(7, 9):
    df1 = counting_break_upper_band_after_n(i, 10)
    lib2.head_offset = 0
    df1 = dr5.get_a_across_b(df1, period_of_days=5, cross_above=("close", "middle"), cross_type="binary-cmp",
                             period_type='week')
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_type="ma5-gt-ma10-gt-m20", period_type='week')
    df1.to_csv("test_" + '_offset_' + str(i) + ".csv")
"""
def counting_slow_semi_break_upper_band_after_n(offset=0, n = 3, k = 10, type='day'):
    df1 = None
    for i in range(n):
        lib2.head_offset = i
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("upper", "high"), cross_type="binary-cmp-close",
                                 period_type=type, rank=True)
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above="upper", cross_type="unary-cmp-self",
                                 period_type=type, rank=True)
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above="high", cross_type="unary-cmp-self",
                                 period_type=type, rank=True)

    df1 = dr5.get_a_across_b(df1, period_of_days=5, cross_above=("close", "ma5"), cross_type="binary-cmp",
                              period_type='day')

def counting_slow_break_upper_band(offset=0, above=2, touch=2, below=8, type='60'):
    df1 = None
    lib2.head_offset = above + 2
    df1 = dr5.get_a_across_b(df1, period_of_days=below, cross_above=("upper", "high"), cross_type="binary-cmp",
                                 period_type='60')

    lib2.head_offset = above
    df1 = dr5.get_a_across_b(df1, period_of_days=touch, cross_above=("high", "upper"), cross_type="binary-cmp",
                             period_type='60')
    df1 = dr5.get_a_across_b(df1, period_of_days=touch, cross_above=("upper", "close"), cross_type="binary-cmp",
                             period_type='60')

    lib2.head_offset = 0
    df1 = dr5.get_a_across_b(df1, period_of_days=above, cross_above=("close", "upper"), cross_type="binary-cmp",
                                 period_type='60')
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_slow_break_upper_band" + type + '_offset_' + str(offset) + '-' + str_time + ".csv")
    return df1

#counting_slow_semi_break_upper_band_after_n(n=3)
#counting_break_upper_band_after_n()

def counting_above_ma5(df1=None):
    df1 = dr5.get_a_across_b(df1, period_of_days=4, cross_above=("close", "ma5"), cross_type="binary-cmp",
                         period_type='day')
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_above_ma5_" + str_time + ".csv")
    return df1

#counting_break_upper_band_after_n()
#df = myapi.read_csv("case/case-boll/break_upper.csv")
#counting_above_ma5(df)

def counting_ma20_go_up():
    df = dr5.get_a_across_b(period_of_days=120, cross_above="ma20", cross_type="unary-current-trend",
                             period_type='day')
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    #df = myapi.read_csv("case/case-boll/current_trend.csv")
    df_pos = df[df['p1'] > 3]
    df_pos = df_pos.sort_values("p1", ascending=False)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df_pos.to_csv("current_trend_pos_" + str_time + '.csv')
    df_neg = df[df['p1'] < -3]
    df_neg = df_neg.sort_values("p1", ascending=True)
    df_neg.to_csv("current_trend_neg_" + str_time + '.csv')
    df_tran = df[(df['p1'] <= 3) & (df['p1'] >= -3)]
    df_tran = df_tran.sort_values("p1", ascending=False)
    df_tran.to_csv("current_trend_tran_" + str_time + '.csv')
    df.to_csv("current_trend" + str_time + ".csv")
    return df1

#counting_ma20_go_up()
#counting_slow_break_upper_band(touch=0)

df1 = myapi.read_csv("case/case-boll/60_breakthrough_upper.csv")
df1 = dr5.get_a_across_b(df1, period_of_days=10, cross_above=("ma20", "lower"), cross_type="unary-cmp-self",
                         period_type='day')
df1.to_csv("ma20-day-down-60-boll-break.csv")