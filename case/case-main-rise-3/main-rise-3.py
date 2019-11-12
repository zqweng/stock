import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi

#3 weeks of flat perod after a big rise, then the last week it rise up
lib2.head_offset = 4
df1 = dr5.get_minimum_price_sum_in_n(period_of_days=10, price_up_sum=30, min_day_range=6, period_type='week')
lib2.head_offset = 0
df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(8, 15), period_type='week')
lib2.head_offset = 1
df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=3, p_change=(-5, 5), period_type='week')

#df1 = dr5.get_price_up_with_percentage(df1, period_of_days=8, p_change=(7, 11), period_type='day')
