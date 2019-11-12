import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi

#3 weeks of flat perod after a big rise, then the last week it rise up
#lib2.head_offset = 4
#df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(8, 15))

for i in range(3, 7):
   lib2.head_offset = 0
   df1 = dr5.get_maximum_price_sum_in_n(period_of_days=i, p_change=(-3, 3), period_type='day')
   lib2.head_offset = i
   df2 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(7, 11), period_type='day')
