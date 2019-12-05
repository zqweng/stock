import driver5 as dr5
import stock_library2 as lib2
import pandas as pd
import datetime

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

#one_week_up_after_many_week_flat()
jump_open_week()