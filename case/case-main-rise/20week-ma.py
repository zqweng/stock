import update_history as uh1
import case_get_hitory_high as hh
import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import pdb
import inspect

## study weekly price across ma20 and seek chance
# df1 = dr5.get_minimum_price_sum_in_n(is_price_up=False, price_up_sum=-10, period_of_days=10, period_type='week')
# df1 = myapi.read_csv("newlist.csv")
# df = myapi.read_csv("basic-no3.csv")
# df2 = lib2.filter_stock(df, df1, "outstanding", 5)
# pdb.set_trace()

"""
lib2.head_offset = 1
df1 = dr5.get_minimum_price_sum_in_n(price_up_sum=16, period_of_days=5, period_type='day')
lib2.head_offset = 0
df1 = dr5.get_maximum_price_sum_in_n(df1, period_of_days=1, p_change=(-10, 0), period_type='day')
df = myapi.read_csv("basic-no3.csv")
df2 = lib2.filter_stock(df, df1, "outstanding", 5)
"""
# df1 = dr5.get_a_across_b(df1, period_of_days=4, period_type='week')
# myapi.market="usa"
# df1 = myapi.read_csv(r"case\case-main-rise\ma20-up-list-us.csv")
# df1 = myapi.read_csv("ma20-up-list-us.csv")
# df1 = myapi.read_csv(r"case\case-main-rise\ma20-is-around-20-30.csv")


"""
   create a stock list that ma20 is continuing going up, the list will be saved to root dir and the file is sorted
   by the number of days that ma20 go up in succession.  
"""
def create_ma20_up_list(market='usa', stock_list="us_stock_volume.csv"):
    myapi.market = market
    df = dr5.get_a_across_b(period_of_days=100, cross_above=("up", "ma20"), cross_type="unary-current-trend",
                            period_type='day', stock_list=stock_list)
    df = df.sort_values("p1", ascending=False)
    df.to_csv("{}-ma20-up-list.csv".format(market))


"""
   current ma5 is up above ma10 while yesterday it was below ma10 
"""


def ma5_cross_above_ma10(df, market='usa'):
    myapi.market = market
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma5", "ma10"), cross_type="binary-cmp",
                            period_type='day')
    lib2.head_offset = 1
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma10", "ma5"), cross_type="binary-cmp",
                            period_type='day')
    df.to_csv("{}.csv".format(inspect.stack()[0][3]))
    return df


"""
   current close price is up above ma20 while yesterday it was below ma20 
"""


def close_cross_above_ma20(df, market='usa'):
    myapi.market = market
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp",
                            period_type='day')
    lib2.head_offset = 1
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "close"), cross_type="binary-cmp",
                            period_type='day')
    return df


"""
   touch base ma20
"""
def close_cross_above_ma20(df, market='usa'):

    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp",
                            period_type='day')
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low"), cross_type="binary-cmp",
                            period_type='day')
    return df


"""
   first time in recent 5 days that close price stand above upper band
   for binary-cmp, period_of_days specifies the period that the result of comparisons should all be true.
"""
def first_cross_above_upper(df, market='usa'):
    myapi.market = market
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                            period_type='day')
    lib2.head_offset = 1
    df1 = dr5.get_a_across_b(df, period_of_days=5, cross_above=("upper", "close"), cross_type="binary-cmp",
                             period_type='day')
    df.to_csv("{}.csv".format(inspect.stack()[0][3]))
    return df

df1 = myapi.read_csv(r"case\case-main-rise\usa-ma20-up-list.csv")
df1 = first_cross_above_upper(df1)
pdb.set_trace()


#create_ma20_up_list()

"""
df = myapi.read_csv("basic-no3.csv")
df1 = myapi.read_csv("ma20-up-list.csv", local=True)
df1 = lib2.filter_stock(df, df1, "outstanding", 5)
pdb.set_trace()
df1.to_csv("ma20-up-list.csv")
"""
