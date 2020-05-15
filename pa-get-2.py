# 获取所有上市公司详细财务报表从网易
import requests
from bs4 import BeautifulSoup
import pandas
import time

import pdb
import time
from os import path

#df_stock_list = pandas.read_csv("new_stock_list.csv", converters={"code": lambda x :str(x)})
df_stock_list = pandas.read_csv("basic-no3.csv", converters={"code": lambda x :str(x)})
"""
for row in df_stock_list.itertuples():

    code_len = len(row.code)
    if code_len < 6:
        prefix = "0" * (6-code_len)
        print("add {} to {}".format(prefix, row.code))
        df_stock_list.at[row.Index,"code"] = prefix + row.code

pdb.set_trace()
"""
for row in df_stock_list.itertuples():

    print(row)

    if path.exists("财报/{}.csv".format(row.name)):
        print("{} exist".format(row.name))
        continue

    res = requests.get("http://quotes.money.163.com/f10/lrb_{}.html".format(row.code))
    soup = BeautifulSoup(res.content, features="lxml")
    tab0 = soup.find("table", {"class": "table_bg001 border_box limit_sale"})
    tab1 = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})

    # from beautifulsoup tag to html, using str()
    tab0_html = str(tab0)
    df0 = pandas.read_html(tab0_html)

    tab1_html = str(tab1)
    df1 = pandas.read_html(tab1_html)

    df = pandas.concat([df0[0],df1[0]], axis=1)
    df.to_csv("财报/{}.csv".format(row.code))
    time.sleep(0.5)

