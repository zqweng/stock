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

    """
    for j in range(k):
        lib2.head_offset = n + j
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                                 period_type=type)
    """
    df1.to_csv("counting_slow_semi_break_upper_band_after_n_" + type + '_offset_' + str(offset) + '_days_' + str(n) + ".csv")
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
df = myapi.read_csv("case/case-boll/break_upper.csv")
counting_above_ma5(df)