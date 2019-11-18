import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import pdb
import pandas as pd
import datetime


# 3 weeks of flat perod after a big rise, then the last week it rise up
# lib2.head_offset = 4
# df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(8, 15))

def day_rise():
    for i in range(3, 7):
        lib2.head_offset = 0
        df1 = dr5.get_maximum_price_sum_in_n(period_of_days=i, p_change=(-3, 3), period_type='day')
        lib2.head_offset = i
        df2 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(7, 11), period_type='day')


def day_break_high():
    df1 = dr5.get_maximum_period_break_high(period_of_days=4, min_break_num=3)
    df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_type="ma5-ma10", period_type='day')
    df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_type="close-ma20", period_type='day')
    # df1 = dr5.get_price_up_with_percentage(df1, period_of_days=3, p_change=(4, 10), period_type='day')
    return df1


def jump_open(type):
    df1 = dr5.get_a_across_b(period_of_days=1, cross_type="jump-open", period_type=type)
    return df1


def small_up_and_drop_with_low_volume():
    df1 = None
    for i in range(1, 4):
        lib2.head_offset = lib2.head_offset + 1
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(0.01, 4), period_type='day')

    lib2.head_offset = lib2.head_offset - 3
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-4, 0), period_type='day')
    df1 = dr5.get_minimum_price_sum_in_n(df1, price_up_sum=3, period_of_days=4)
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_type="volume-drop")
    df1 = dr5.get_a_across_b(df1, period_of_days=4, cross_type="close-ma20", period_type='day')
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_type="abs-pchange-less", period_type='day')
    return df1


# jump_open('day')
df_list = []
for i in range(0, 9):
    lib2.head_offset = i
    df1 = small_up_and_drop_with_low_volume()
    print(df1)
    df_list.append(df1)

df_concat = pd.concat(df_list)
df_concat.to_csv("result-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv")

df1 = dr5.get_a_across_b(df1, (), cross_type="verify-pchange")


# follow the example of 博通股份 2019-11-06
#complex_small_up()

#dr5.get_history_high_price(event_to_now=1, period_of_days=60)