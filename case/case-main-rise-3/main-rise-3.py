import stock_library2 as lib2
import driver5 as dr5
import pdb

#3 weeks of flat perod after a big rise, then the last week it rise up
df1 = None
lib2.head_offset = 3
#df1 = dr5.get_minimum_price_sum_in_n(df1, period_of_days=3, price_up_sum=12, min_day_range=2, period_type='week')
#lib2.head_offset = 0
#df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(8, 15), period_type='week')
lib2.head_offset = 1
#df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=3, p_change=(-4, 4), period_type='week')

df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(40, 100), period_type='week')
pdb.set_trace()