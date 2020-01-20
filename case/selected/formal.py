import driver5 as dr5
import stock_library2 as lib2
import pandas as pd
import datetime
import pdb

def one_week_up_after_many_week_flat():
    df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(10, 15), period_type='week')
    lib2.head_offset = 1
    df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=3, p_change=(-5, 9), period_type='week')
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv('onw_week_up_after_many_week_flat_' + str_time + '.csv')

def jump_open_week():
    ## p_change > 10 and above m20, a good chance for next week
    ## drop down after peek, it touch the bottom in the early morning in the following days when it can be easily beat down.
    ## when you see the big buy, it is time to go in
    lib2.head_offset = 0
    df1 = dr5.get_a_across_b(period_of_days=1, cross_type="jump-open", period_type="week")
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv('jump_open_week' + str_time + '.csv')

"""
   suppose stock should stand above boll upper price for two period of time to confirm it up rally. and 2 period before this, we dont know but we call it touch time,
   but prior to touch time, there should be at least 8 period of silence time  
"""
def counting_slow_break_upper_band(offset=0, above=2, touch=0, below=8, type='60'):
    df1 = None
    lib2.head_offset = above + 2 + offset
    df1 = dr5.get_a_across_b(df1, period_of_days=below, cross_above=("upper", "high"), cross_type="binary-cmp",
                                 period_type='60')

    lib2.head_offset = above + offset
    df1 = dr5.get_a_across_b(df1, period_of_days=touch, cross_above=("high", "upper"), cross_type="binary-cmp",
                             period_type='60')
    df1 = dr5.get_a_across_b(df1, period_of_days=touch, cross_above=("upper", "close"), cross_type="binary-cmp",
                             period_type='60')

    lib2.head_offset = 0 + offset
    df1 = dr5.get_a_across_b(df1, period_of_days=above, cross_above=("close", "upper"), cross_type="binary-cmp",
                                 period_type='60')


    lib2.head_offset = 0 + offset
    df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_above=("close", "middle"), cross_type="binary-cmp",
                             period_type='day')

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_slow_break_upper_band" + type + '_offset_' + str(offset) + '-' + str_time + ".csv")
    return df1

def counting_break_upper_band_after_n(offset=0, num = 8, type='day',  df1=None):
    lib2.head_offset = offset
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                             period_type=type, rank=True)

    #pdb.set_trace()

    for i in range(1, num):
        lib2.head_offset = i + offset
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("upper", "close"), cross_type="binary-cmp",
                                 period_type=type)

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df1.to_csv("counting_close_above_upper_" + type + '-' + str_time + '_offset_' + str(offset) + '_days_' + str(num) + ".csv")
    return df1


#one_week_up_after_many_week_flat()
#jump_open_week()

"""
长期在20日线下，但是20小时线获得突破，小时线突破布林上轨，预示着20日线即将向上，走上上升通道
df1 = counting_slow_break_upper_band(touch=0)
df1 = dr5.get_a_across_b(df1, period_of_days=10, cross_above=("ma20", "lower"), cross_type="unary-cmp-self",
                         period_type='day')
"""
def test(offset=0):
    df1 = counting_slow_break_upper_band(offset=offset, touch=0)
    lib2.head_offset = 4 + offset
    df2 = dr5.get_a_across_b(df1, period_of_days=8, cross_above=("ma20", "greater"), cross_type="unary-cmp-self",
                             period_type='60')
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df2.to_csv("second_breakthrough_60_" + 'offset_' + str(offset) + '_' + str_time + ".csv")


#test(offset=2)

#counting_slow_break_upper_band()
counting_break_upper_band_after_n()