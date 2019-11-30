import update_history as uh1
import case_get_hitory_high as hh
import driver5 as dr5
import api as myapi
import pdb
import stock_library2 as lib2

def one_week_down_after_two_week_up():
    for i in range(0, 2):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(-5, -3), period_type='week')
        lib2.head_offset = i + 1
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(5, 10), period_type='week')
        lib2.head_offset = i + 2
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(5, 10), period_type='week')
"""    
lib2.head_offset = 10
df1 = dr5.get_minimum_price_sum_in_n(price_up_sum=20, period_of_days=5, min_day_range=3, period_type='week')
lib2.head_offset = 0
df1 = dr5.get_minimum_price_sum_in_n(df1, is_price_up=False, price_up_sum=-10, period_of_days=6, period_type='week')

df1 = dr5.get_minimum_price_sum_in_n(df1, price_up_sum=5, period_of_days=2, period_type='week')
#df1 = dr5.get_price_up_with_percentage(df1, period_of_days=4)
#df1 = dr5.get_price_above(df1, type="low below ma20", period_of_days=5, period_type='week')
df1.to_csv("week-rise-and-down-just-rerise-2.csv")
"""
def two_week_down_after_many_week_up():
    for i in range(0, 1):
        lib2.head_offset = i
        df1 = dr5.get_minimum_price_sum_in_n(price_up_sum=-12, is_price_up=False, period_of_days=2, min_day_range=2, period_type='week')
        lib2.head_offset = i + 2
        df1 = dr5.get_minimum_price_sum_in_n(df1, price_up_sum=30, period_of_days=10, min_day_range=8, period_type='week')

def one_week_up_after_many_week_flat():
    df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(10, 15), period_type='week')
    lib2.head_offset = 1
    df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=3, p_change=(-5, 9), period_type='week')


def two_week_up():
    for i in range(2, 4):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(5, 10), period_type='week')
        lib2.head_offset = i + 1
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(10, 20), period_type='week')
        df1.to_csv("two-week-" + str(i) + ".csv")


#one_week_down_after_two_week_up()
#one_week_up_after_many_week_flat()
two_week_up()