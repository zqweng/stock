import update_history as uh1
import case_get_hitory_high as hh
import driver5 as dr5
import api as myapi
import pdb

#uh1.update_day()
#dr5.get_w_shape()
#hh.get_history_high_v2()
#hh.get_one_year_high_v2()
#hh.get_half_year_high_v2()
#hh.get_history_high_volume()
#hh.get_one_year_high_volume()
#dr5.get_current_price_up_periods()df
#dr5.get_current_no_touch_ma5_periods()
#hh.get_first_history_high_volume_in_10_days()
#hh.get_first_one_year_high_volume_in_10_days()
df = dr5.get_price_sum_in_n(price_up_sum=0, stock_list="mystocklist-detail.csv")
#df1 = dr5.get_price_sum_in_n(price_up_sum=0)
#df1 = dr5.get_price_sum_in_n(df1, is_price_up=False, price_up_sum=-15)
#print(df1)
#df = myapi.read_csv("price_sum.csv")
#df1 = dr5.get_price_sum_in_n(df, is_price_up=False, price_up_sum=-10)
#df = dr5.get_price_sum_in_n(price_up_sum=15, period_of_days=15)
#df = myapi.read_csv("price_sum1.csv")
#df = dr5.get_price_continuous_down_in_n(df, num_of_days_down=4, price_down_sum=-7)
#dr5.get_price_continuous_down_in_n(num_of_days_down=4, price_down_sum=-5, period_of_days=6)
#dr5.get_price_continuous_down_in_n(num_of_days_down=5, price_down_sum=-10, period_of_days=10)
print('finish')
