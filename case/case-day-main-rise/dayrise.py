import stock_library2 as lib2
import driver5 as dr5
import pdb


# 3 weeks of flat periods after a big rise, then the last week it rise up
# lib2.head_offset = 4
# df1 = dr5.get_price_up_with_percentage(period_of_days=1, p_change=(8, 15))

def day_rise():
    for i in range(3, 7):
        lib2.head_offset = 0
        df1 = dr5.get_maximum_price_sum_in_n(period_of_days=i, p_change=(-3, 3), period_type='day')
        lib2.head_offset = i
        df2 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(7, 11), period_type='day')


def day_break_high():
    df1 = dr5.get_maximum_period_break_high(period_of_days=4, min_break_num=3)
    df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_type="ma5-ma10", period_type='day')
    df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_type="close-ma20", period_type='day')
    # df1 = dr5.get_price_up_with_percentage(df1, period_of_days=3, p_change=(4, 10), period_type='day')
    return df1


def jump_open(type):
    df1 = dr5.get_a_across_b(period_of_days=1, cross_type="jump-open", period_type=type)
    return df1


def small_up_and_drop_with_low_volume():
    df1 = None
    for i in range(1, 4):
        lib2.head_offset = lib2.head_offset + 1
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(0.01, 4), period_type='day')

    lib2.head_offset = lib2.head_offset - 3
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-4, 0), period_type='day')
    df1 = dr5.get_minimum_price_sum_in_n(df1, price_up_sum=3, period_of_days=4)
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_type="volume-drop")
    df1 = dr5.get_a_across_b(df1, period_of_days=4, cross_type="close-ma20", period_type='day')
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_type="abs-pchange-less", period_type='day')
    return df1

"""
df1 = jump_open('day')
df1 = dr5.get_a_across_b(df1, period_of_days=2, cross_type="close-ma20", period_type='day')
"""

"""
df_list = []
for i in range(0, 9):
    lib2.head_offset = i
    df1 = small_up_and_drop_with_low_volume()
    print(df1)
    df_list.append(df1)

df_concat = pd.concat(df_list)
df_concat.to_csv("result-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv")

df1 = dr5.get_a_across_b(df1, (), cross_type="verify-pchange")
"""

# follow the example of 博通股份 2019-11-06
#complex_small_up()

#dr5.get_history_high_price(event_to_now=1, period_of_days=60)

#day_rise()

def two_days_up_with_4p():
    df1 = None
    for i in range(1, 3):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(4, 11), period_type='day')

    for i in range(3, 7):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-4, 4), period_type='day')


    lib2.head_offset = 0
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-5,0), period_type='day')


def one_days_up_with_4p():
    df1 = None
    for i in range(1, 3):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(2, 3), period_type='day')

    lib2.head_offset = 0
    pdb.set_trace()
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(4, 10), period_type='day')

def one_days_up_with_6p():
    df1 = None
    for i in range(1, 2):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(6, 11), period_type='day')

    for i in range(3, 7):
        lib2.head_offset = i
        df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-4, 4), period_type='day')


    lib2.head_offset = 0
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-2,2), period_type='day')

def two_days_up_with_3_4p():
    df1 = None
    lib2.head_offset = 1
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(3.5, 11), period_type='day')

    lib2.head_offset = 2
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(3.5, 11), period_type='day')

    lib2.head_offset = 0
    df1 = dr5.get_price_up_with_percentage(df1, period_of_days=1, p_change=(-1, 1), period_type='day')

def ma5_gt_ma10_ma20(n, df = None):
    for i in range(n):
        lib2.head_offset = i
        df = dr5.get_a_across_b(df, period_of_days=1, cross_type="ma5-gt-ma10-gt-m20", period_type='day')
    return df

#two_days_up_with_3_4p()

#dr5.get_minimum_price_sum_in_n(price_up_sum=10, period_of_days=3, min_day_range=3)
#dr5.get_minimum_price_sum_in_n(price_up_sum=11, period_of_days=3, min_day_range=3, period_type='week')

#two_days_up_with_3_4p()

#df1 = dr5.get_a_across_b(period_of_days=50, cross_above=(5, 11, 4, 4, 12, 200), cross_type="momentum", period_type='day')

#df1 = dr5.get_a_across_b(period_of_days=20, cross_above=10, cross_type="highest-in-n", period_type='day')
#jump_open("day")

def strong_bounce_from_ma10(i):
    df1 = None
    lib2.head_offset = i
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("ma10", "low"), cross_type="binary-cmp", period_type='day')
    df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "ma5"), cross_type="binary-cmp", period_type='day')

    for j in range(i, 4):
        lib2.head_offset = j + 1
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "ma5"), cross_type="binary-cmp", period_type='day')

    df1 = ma5_gt_ma10_ma20(5, df1)

    df1.to_csv("strong_bounce_ma10" + str(i) + ".csv")

def counting_above_ma5_time(num_of_days = 5, df1 = None):
    df1 = dr5.get_a_across_b(df1, period_of_days=num_of_days, cross_above=("close", "ma5"), cross_type="binary-cmp",
                             period_type='day')



def counting_close_above_ma5(num = 9):
    df1 = None
    for i in range(num):
        lib2.head_offset = i
        df1 = dr5.get_a_across_b(df1, period_of_days=1, cross_above=("close", "ma5"), cross_type="binary-cmp",
                                 period_type='day')
    df1.to_csv("counting_close_above_ma5" + str(num) + ".csv")

def counting_high(num_of_days = 30, df1 = None):
    df1 = dr5.get_a_across_b(df1, period_of_days=num_of_days, cross_above=["close", "volume"], cross_type="unary-cmp",
                             period_type='day')

    df1.to_csv("counting_high" + str(num_of_days) + ".csv")


counting_close_above_ma5()