import baostock as bs
import pandas as pd
import pdb
import api as myapi

def test_fun():
    df_orig = myapi.read_csv(r"mystocklist_detail.csv")
    stock_list=df_orig.index.to_list()
    new_stock_list = ["sz.{}".format(code) if code[0] == '0' else "sh.{}".format(code) for code in stock_list]

    df_all = None

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    for code in new_stock_list:
        #### 获取公司业绩预告 ####
        rs_forecast = bs.query_forecast_report(code, start_date="2020-03-01", end_date="2020-12-31")
        print('query_forecast_reprot respond error_code:'+rs_forecast.error_code)
        print('query_forecast_reprot respond  error_msg:'+rs_forecast.error_msg)
        rs_forecast_list = []
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            # 分页查询，将每页信息合并在一起
            rs_forecast_list.append(rs_forecast.get_row_data())

        df = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)

        if df_all is None:
            df_all = df
        else:
            df_all = pd.concat([df_all, df])

        #### 结果集输出到csv文件 ####
        #result_forecast.to_csv("D:\\forecast_report.csv", encoding="gbk", index=False)
        print(df_all)

    df_all.to_csv(r"result\profit.csv")
    #### 登出系统 ####
    bs.logout()

def test_fun2():
    df_all = None
    df_orig = myapi.read_csv(r"basic-no3.csv")
    stock_list = df_orig.index.to_list()
    new_stock_list = ["sz.{}".format(code) if code[0] == '0' else "sh.{}".format(code) for code in stock_list]
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    for code in new_stock_list:
        #### 获取公司业绩预告 ####
        rs_forecast = bs.query_forecast_report(code, start_date="2019-03-01", end_date="2020-12-31")
        print('query_forecast_reprot respond error_code:' + rs_forecast.error_code)
        print('query_forecast_reprot respond  error_msg:' + rs_forecast.error_msg)
        rs_forecast_list = []
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            # 分页查询，将每页信息合并在一起
            rs_forecast_list.append(rs_forecast.get_row_data())
        if len(rs_forecast_list) == 0:
            continue

        df = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)

        if df_all is None:
            df_all = df
        else:
            df_all = pd.concat([df_all, df])

        #### 结果集输出到csv文件 ####
        # result_forecast.to_csv("D:\\forecast_report.csv", encoding="gbk", index=False)
    print(df_all)
    pdb.set_trace()

    df_all.to_csv(r"result\profit.csv")
    #### 登出系统 ####
    bs.logout()

test_fun2()
"""
df_orig = myapi.read_csv(r"mystocklist_detail.csv")
df_profit =  myapi.read_csv(r"result\mylist.csv")
df = df_orig.loc[df_orig.index.intersection(df_profit.index)]
pdb.set_trace()
"""