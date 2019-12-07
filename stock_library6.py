"""
calculated the added price up or down percentage between any two days in the specified period and return the largest up
or down value according to the value of para1
we will create a list of tuples (index, number, total price change), index is the row index of the dataframe, number is
the number of days , total price change is the price change in those number of days.
then we will use sorted function to sort the list and return largest or smallest values

para1:  determine whether we want price up or down values
"""
import pdb


def find_minimum_price_sum_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    list = []
    for i in range(latest_n_days):
        for j in range(0, latest_n_days - i):
            list.append((i, j + 1, df[i: i + j + 1]["p_change"].sum()))

    ordered_list = sorted(list, key=lambda x: x[2], reverse=para1)
    index, num_of_days, p_chane_sum = ordered_list[0]

    # if code == "002508":
    #    pdb.set_trace()
    # para2[1] is the least maximum days
    if para2[1] != 0 and num_of_days < para2[1]:
        return True

    if para2[0] != 0:
        # para1 true means up is needed and the p_change_sum must be greater than para2
        # same for the reverse case
        if (para1 and para2[0] > p_chane_sum) or (not para1 and para2[0] < p_chane_sum):
            return True

    if num_of_days > 0:
        result_list.append(tuple((name, code, df.loc[index].date,
                                  df.loc[index + num_of_days - 1].date,
                                  num_of_days, p_chane_sum)))
    return True


def find_maximum_price_sum_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    list = []
    for i in range(latest_n_days):
        for j in range(0, latest_n_days - i):
            list.append((i, j, df[i: i + j + 1]["p_change"].sum()))

    ordered_list = sorted(list, key=lambda x: x[2])

    index, num_of_days, p_chane_sum_max = ordered_list[0]
    index1, num_of_days1, p_chane_sum_min = ordered_list[-1]

    if para1[0] <= p_chane_sum_max <= para1[1] and para1[0] <= p_chane_sum_min <= para1[1]:
        result_list.append(tuple((name, code, 0,
                                  0,
                                  num_of_days, 0)))
    return True


def find_price_continuous_down_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    num_of_days_down = 0
    change_sum = 0
    index = -1
    for i in range(latest_n_days):
        if df.loc[i].p_change >= 0:
            if num_of_days_down >= para1:
                break
            else:
                num_of_days_down = 0;
                continue
        else:
            if num_of_days_down == 0:
                index = i
            num_of_days_down = num_of_days_down + 1
            change_sum = change_sum + df.loc[i].p_change
    # pdb.set_trace()
    if num_of_days_down >= para1 and para2 != 0 and para2 <= change_sum:
        result_list.append(tuple((name, code, df.loc[index].date,
                                  df.loc[index + num_of_days_down - 1].date,
                                  0, 0)))
    return True


"""
def find_ma5_cross_ma10(df, name, code, latest_n_days, result_list, para1, para2):
    for i in range(latest_n_days):
        if (not para1 and (df.loc[i].ma5 < df.loc[i].ma10 and df.loc[i + 1].ma5 >= df.loc[i + 1].ma10)) or (
                para1 and (df.loc[i].ma5 > df.loc[i].ma10 and df.loc[i + 1].ma5 <= df.loc[i + 1].ma10)):
            result_list.append(tuple((name, code, df.loc[i].date,
                                      df.loc[i + 1].date,
                                      latest_n_days, 0)))
            return True
"""


def check_close_ma20(df, i, para1):
    return (not para1 and (df.loc[i].close < df.loc[i].ma20 and df.loc[i + 1].close >= df.loc[i + 1].ma20)) or (
            para1 and (df.loc[i].close > df.loc[i].ma20 and df.loc[i + 1].close <= df.loc[i + 1].ma20))


def check_ma5_ma10(df, i, para1):
    return (not para1 and (df.loc[i].ma5 < df.loc[i].ma10 and df.loc[i + 1].ma5 >= df.loc[i + 1].ma10)) or (
            para1 and (df.loc[i].ma5 > df.loc[i].ma10 and df.loc[i + 1].ma5 <= df.loc[i + 1].ma10))

def check_jump_open(df, i):
    return df.loc[i].low > df.loc[i + 1].high

def check_volume_drop(df, i):
    return df.loc[i].volume < df.loc[i+1].volume * 0.7

def check_abs_pchange_less(df, i):
    return abs(df.loc[i].p_change) < abs(df.loc[i+1].p_change)

def check_momentum(df, i, para1):
    money = df.loc[i].volume * df.loc[i].close
    return (para1[1] >= df.loc[i].p_change >= para1[0] and money/100000000 > para1[2] and
            para1[4] >= df.loc[i].turn >= para1[3] and
            money/100000000 * 100/df.loc[i].turn >= para1[5])

def check_highest_in_n(df, i, para1):
    return df.loc[i].close > max(max(df[1:para1]["close"]), df.loc[i].ma20)

def check_ma5_gt_ma10_gt_ma20(df, i):
    return df.loc[i].ma5 > df.loc[i].ma10 > df.loc[i].ma20

def check_binary_cmp(df, i, para1):
    return df.loc[i][para1[0]] >= df.loc[i][para1[1]]

def check_binary_cmp_close(df, i, para1):
    return abs((df.loc[i][para1[0]] - df.loc[i][para1[1]])/df.loc[i][para1[1]]) <= 0.025

def check_unary_cmp(df, num, para1):
    for col in para1:
        if df.loc[0][col] <= max(df[1:num][col]):
            return False
    return True

def check_unary_cmp_self(df, i, para1):
    if para1[1] == "greater":
        return df.loc[i][para1[0]] > df.loc[i+1][para1[0]]
    else:
        return df.loc[i][para1[0]] < df.loc[i+1][para1[0]]

def find_a_cross_b(df, name, code, latest_n_days, result_list, para1, para2):
    if para2 == "verify-pchange":
        ret = check_abs_pchange_less(df, para1)
        result_list.append(tuple((name, code, para1[0], ret[0], ret[1])))
        return True

    if para2 == "highest-in-n" and check_highest_in_n(df, 0, para1):
        result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, 0,0,0,0)))
        return True

    if para2 == "binary-cmp":
        for i in range(latest_n_days):
            if not check_binary_cmp(df, i, para1):
                return False
        result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, 0, 0, 0, 0)))
        return True

    if para2 == "binary-cmp-close":
        for i in range(latest_n_days):
            if not check_binary_cmp_close(df, i, para1):
                return False
        result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, 0, 0, 0, 0)))
        return True

    if para2 == "unary-cmp-self":
        for i in range(latest_n_days):
            if not check_unary_cmp_self(df, i, para1):
                return False
        result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, 0, 0, 0, 0)))
        return True

    if para2 == "unary-current-trend":
        count = 1
        if df.loc[0][para1] >= df.loc[1][para1]:
            go_up = True
        else:
            go_up = False
        for i in range(1, latest_n_days):
            if (df.loc[i][para1] >= df.loc[i+1][para1]) == go_up:
                count = count + 1
            else:
                break
        if not go_up:
            count = -count
        print(code, ' count ', count)
        result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, 0, count, 0, 0)))
        return True

    if para2 == "unary-cmp":
        if check_unary_cmp(df, latest_n_days, para1):
            result_list.append(tuple((name, code, df.loc[0].date, 0, latest_n_days, latest_n_days, 0, 0, 0)))
        return True

    for i in range(latest_n_days):
        if para2 == "momentum" and i != 0 and check_momentum(df, i, para1):
            result_list.append(tuple((name, code, df.loc[i].date, df.loc[i + 1].date, latest_n_days,
                                      0, df.loc[i].p_change,
                                      df.loc[i].volume * df.loc[i].close/100000000,
                                      df.loc[i-1].p_change)))
        elif ((para2 == "close-ma20" and check_close_ma20(df, i, para1)) or
            (para2 == "ma5-ma10" and check_ma5_ma10(df, i, para1)) or
            (para2 == "jump-open" and check_jump_open(df, i)) or
            (para2 == "volume-drop" and check_volume_drop(df, i)) or
            (para2 == "abs-pchange-less" and check_abs_pchange_less(df, i)) or
            (para2 == "ma5-gt-ma10-gt-m20" and check_ma5_gt_ma10_gt_ma20(df, i)) or
            (para2 == "binary-cmp" and check_binary_cmp(df, i, para1))
        ):
            result_list.append(tuple((name, code, df.loc[i].date, df.loc[i + 1].date, latest_n_days, 0, 0, 0, 0)))
            return True


def find_price_above(df, name, code, latest_n_days, result_list, para1, para2):
    for i in range(latest_n_days):
        if (para1 == "close above ma20" and df.loc[i].close > df.loc[i].ma20) or (
                para1 == "low below ma20" and df.loc[i].low < df.loc[i].ma20):
            result_list.append(tuple((name, code, df.loc[i].date,
                                      df.loc[i + 1].date,
                                      latest_n_days, 0)))
            return True


def find_price_up_with_percentage(df, name, code, latest_n_days, result_list, para1, para2):
    for i in range(latest_n_days):
        if para1[1] >= df.loc[i].p_change >= para1[0]:
            result_list.append(tuple((name, code, df.loc[i].date, 0, latest_n_days, 0)))
            return True
