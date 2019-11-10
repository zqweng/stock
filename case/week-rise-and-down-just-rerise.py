import update_history as uh1
import case_get_hitory_high as hh
import driver5 as dr5
import api as myapi
import pdb
import stock_library2 as lib2
lib2.head_offset = 10
df1 = dr5.get_price_sum_in_n(price_up_sum=30, period_of_days=20, min_day_range=6, period_type='week')
lib2.head_offset = 0
df1 = dr5.get_price_sum_in_n(df1, is_price_up=False, price_up_sum=-10, period_of_days=6, period_type='week')

df1 = dr5.get_price_sum_in_n(df1, price_up_sum=5, period_of_days=2, period_type='week')
#df1 = dr5.get_price_up_with_percentage(df1, period_of_days=4)
#df1 = dr5.get_price_above(df1, type="low below ma20", period_of_days=5, period_type='week')
df1.to_csv("week-rise-and-down-just-rerise-2.csv")