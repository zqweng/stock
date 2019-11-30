import driver5 as dr5
import stock_library2 as lib2


def one_week_up_after_many_week_flat():
    df1 = None
    df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(10, 15), period_type='week')
    lib2.head_offset = 1
    df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=3, p_change=(-5, 9), period_type='week')

dr5.get_a_across_b(period_of_days=1, cross_type="jump-open", period_type="week")
one_week_up_after_many_week_flat()