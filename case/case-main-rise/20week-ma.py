import stock_library2 as lib2
import driver5 as dr5
import api as myapi
import pdb
import inspect

"""
   create a stock list that ma20 is continuing going up, the list will be saved to root dir and the file is sorted
   by the number of days that ma20 go up in succession.  
"""


def create_ma20_up_list(market='usa', stock_list="us_stock_volume.csv"):
    myapi.market = market
    df = dr5.get_a_across_b(period_of_days=100, cross_above=("up", "ma20"), cross_type="unary-current-trend",
                            period_type='day', stock_list=stock_list)
    df = df.sort_values("p1", ascending=False)
    df.to_csv("{}-ma20-up-list2.csv".format(market))

def create_ma5_ma10_ma20_list(market='usa', stock_list="us_stock_volume.csv"):
    myapi.market = market
    df = dr5.get_a_across_b(period_of_days=1, cross_above=("ma5", "ma10"), cross_type="binary-cmp",
                            period_type='day', stock_list=stock_list)
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp",
                            period_type='day')
    df.to_csv("{}_{}.csv".format(market, inspect.stack()[0][3]))

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


def close_cross_above_ma20(df, market='usa', offset=0):
    myapi.market = market
    lib2.head_offset = offset
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp",
                            period_type='day')
    lib2.head_offset = 1 + offset
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "close"), cross_type="binary-cmp",
                            period_type='day')
    df.to_csv("{}-off-{}.csv".format(inspect.stack()[0][3], offset))
    return df


"""
   touch base ma20
"""


def touch_base_ma20(df, market='usa'):
    myapi.market = market
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp",
                            period_type='day')
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low"), cross_type="binary-cmp",
                            period_type='day')
    df.to_csv("{}.csv".format(inspect.stack()[0][3]))
    return df


"""
   first time in recent 5 days that close price stand above upper band
   for binary-cmp, period_of_days specifies the period that the result of comparisons should all be true.
   "0.02" means upper price must rise up above 2% than yesterday. since upper price is a average one so 2% rise should
   be a huge change. 
"""
def first_cross_above_upper(df, market='usa', period='day', offset=0, silence=5, rise=0):
    myapi.market = market
    lib2.head_offset = offset
    if rise >= 0:
        df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "close", rise), cross_type="binary-cmp",
                                period_type=period)
    df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "upper"), cross_type="binary-cmp",
                            period_type=period)
    lib2.head_offset = 1 + offset
    df = dr5.get_a_across_b(df, period_of_days=silence, cross_above=("upper", "close"), cross_type="binary-cmp",
                            period_type=period)

    df.to_csv("{}_pe_{}_offset_{}.csv".format(inspect.stack()[0][3], period, offset))
    return df

def width_less(df, market='usa', period='day', offset=0):
    myapi.market = market
    lib2.head_offset = offset
    df = dr5.get_a_across_b(df, period_of_days=2, cross_above="width", cross_type="unary-cmp",
                            period_type=period)
    df.to_csv("{}_pe_{}_offset_{}.csv".format(inspect.stack()[0][3], period, offset))
    return df

#create_ma20_up_list()

def get_result():
    df = myapi.read_csv(r"case\case-main-rise\usa-ma20-up-list2.csv")
    for i in range(3, 5):
        df1 = first_cross_above_upper(df, rise=0.03, offset=i, silence=10)
        df1 = width_less(df1, market='usa', period='day', offset=i+1)


def get_result_60m():
    df1 = myapi.read_csv(r"case\case-main-rise\usa_create_ma5_ma10_ma20_list.csv")
    for i in range(13,20):
        first_cross_above_upper(df1, period='60m', silence=20, offset=i, rise=0.02)


#get_result()
#get_result_60m()
#create_ma5_ma10_ma20_list()

#df1 = myapi.read_csv(r"case\case-main-rise\usa-ma20-up-list2.csv")
#df1 = first_cross_above_upper(df1, rise=0.03, offset=2, silence=10)
#df1 = upper_turn(df1, market='usa', period='day', offset=3)
#pdb.set_trace()
"""
df = dr5.get_a_across_b(period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp",
                        period_type='day')
df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("ma20", "low", 0.01, 0.01), cross_type="binary-cmp",
                            period_type='day')
df.to_csv("ma20-1.csv")
"""
"""
df1 = myapi.read_csv(r"case\case-main-rise\ma20-1.csv")
df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(6, 11), period_type='day')
df1.to_csv("ma20-6p-1.csv")
"""
"""
df = myapi.read_csv("basic-no3.csv")
df = df[df['outstanding'] <=5]
pdb.set_trace()

df1 = myapi.read_csv(r"case\case-main-rise\ma20-6p-1.csv")
pdb.set_trace()
df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("ma5", "ma20"), cross_type="binary-cmp")
df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("ma10", "ma20"), cross_type="binary-cmp")
pdb.set_trace()
"""
df = myapi.read_csv("basic-no3.csv")
df = df[df['outstanding'] <=2]
df1 = myapi.read_csv(r"case\case-main-rise\ma20-6p-1.csv")
common = df1.index.intersection(df.index)
df1 = df1.loc[common]
pdb.set_trace()