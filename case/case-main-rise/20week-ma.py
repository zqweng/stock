import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import pdb
## study weekly price across ma20 and seek chance
df1 = dr5.get_minimum_price_sum_in_n(is_price_up=False, price_up_sum=-10, period_of_days=10, period_type='week')
df1 = dr5.get_minimum_price_sum_in_n(df1, price_up_sum=10, period_of_days=4, period_type='week')
df1 = dr5.get_a_across_b(df1, period_of_days=4, period_type='week')
#df1 = myapi.read_csv("get_price.csv")

