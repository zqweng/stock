import pdb

def find_current_price_up_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    price_up_num = 0
    for i in range(latest_n_days):
        if df.loc[i].p_change <= 0:
            if price_up_num >= 2:
                result_list.append(tuple((name, code, df.loc[i - 1].date,
                                          df.loc[0].date,
                                          price_up_num, 0)))
            return
        else:
            price_up_num = price_up_num + 1

    return True

def find_current_no_touch_ma5_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    price_up_num = 0
    for i in range(latest_n_days):
        if df.loc[i].ma5 >= df.loc[i].low:
            if price_up_num >= 3:
                result_list.append(tuple((name, code, df.loc[i - 1].date,
                                          df.loc[0].date,
                                          price_up_num, 0)))
            return
        else:
            price_up_num = price_up_num + 1

def find_maximum_period_break_high(df, name, code, latest_n_days, result_list, para1, para2):
    num_of_break = 0
    maximum_num_of_break = 0
    for i in range(latest_n_days):
        if df.loc[i].high > df.loc[i+1].high:
            num_of_break = num_of_break + 1
        else:
            if num_of_break > maximum_num_of_break:
                maximum_num_of_break = num_of_break
            if num_of_break > 0:
                num_of_break = num_of_break - 1
            else:
                num_of_break = 0

    if i == latest_n_days and maximum_num_of_break == 0 and num_of_break > 0:
        maximum_num_of_break = num_of_break
    if maximum_num_of_break >= para1:
        result_list.append(tuple((name, code, 0, 0, maximum_num_of_break, 0)))
    return True