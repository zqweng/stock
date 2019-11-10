import update_history as uh1
import case_get_hitory_high as hh
import driver5 as dr5
import api as myapi
import pdb
df1 = dr5.get_price_sum_in_n(price_up_sum=30, period_of_days=20, period_type='week')
df1 = dr5.get_price_sum_in_n(df1, is_price_up=False, price_up_sum=-10, period_of_days=10, period_type='week')
#df1 = myapi.read_csv("up-20-down-10-in-20days.csv")
df1 = dr5.get_ma5_across_ma10(df1, cross_above=False, period_of_days=4, period_type='week')
df1 = dr5.get_price_above(df1, type="close above ma20", period_of_days=1, period_type='week')
#df1 = dr5.get_price_up_with_percentage(df1, period_of_days=4)
df1 = dr5.get_price_above(df1, type="low below ma20", period_of_days=5, period_type='week')
df1.to_csv("week-rise-and-down.csv")