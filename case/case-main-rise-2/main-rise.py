import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi

df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(0, 4), period_type='week')
lib2.head_offset = 1
df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(10, 15), period_type='week')
lib2.head_offset = 0
