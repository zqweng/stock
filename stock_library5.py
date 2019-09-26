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
