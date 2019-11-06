"""
calculated the added price up or down percentage between any two days in the specified period and return the largest up
or down value according to the value of para1
we will create a list of tuples (index, number, total price change), index is the row index of the dataframe, number is
the number of days , total price change is the price change in those number of days.
then we will use sorted function to sort the list and return largest or smallest values

para1:  determine whether we want price up or down values
"""
import pdb


def find_price_up_sum_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    list = []
    for i in range(latest_n_days):
        for j in range(0, latest_n_days - i):
            list.append((i, j, df[i: i + j + 1]["p_change"].sum()))

    ordered_list = sorted(list, key=lambda x: x[2], reverse=para1)
    index, num_of_days, p_chane_sum = ordered_list[0]

    if para2 != 0:
        # para1 true means up is needed and the p_change_sum must be greater than para2
        # same for the reverse case
        if (para1 and para2 > p_chane_sum) or (not para1 and para2 < p_chane_sum):
            return True

    # pdb.set_trace()
    if num_of_days > 0:
        result_list.append(tuple((name, code, df.loc[index].date,
                                  df.loc[index + num_of_days - 1].date,
                                  num_of_days, p_chane_sum)))
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
    #pdb.set_trace()
    if num_of_days_down >= para1 and para2 != 0 and para2 <= change_sum:
        result_list.append(tuple((name, code, df.loc[index].date,
                                  df.loc[index + num_of_days_down - 1].date,
                                  0, 0)))
    return True
