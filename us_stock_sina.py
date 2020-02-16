# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/30 18:47
contact: jindaxiang@163.com
desc: 获取新浪财经-美股实时行情数据和历史行情数据
优化: 在美股行情的获取上采用多线程模式(新浪会封IP, 不再优化)
"""
import pdb
import time
import json

import requests
import pandas as pd
import execjs

from akshare.stock.cons import (js_hash_text,
                                hk_js_decode,
                                us_sina_stock_list_url,
                                us_sina_stock_dict_payload,
                                us_sina_stock_hist_url,
                                us_sina_stock_hist_qfq_url)


def get_us_page_count():
    page = "1"
    us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
    js_code = execjs.compile(js_hash_text)
    dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
    us_sina_stock_dict_payload.update({"page": "{}".format(page)})
    res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
    data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
    if not isinstance(int(data_json["count"]) / 20, int):
        page_count = int(int(data_json["count"]) / 20) + 1
    else:
        page_count = int(int(data_json["count"]) / 20)
    return page_count


def stock_us_spot():
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    #page_count = 1
    for page in range(1, page_count+1):
        # page = "1"
        print("正在抓取第{}页的美股数据".format(page))
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        print(us_sina_stock_dict_payload)
        res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
        data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
        big_df = big_df.append(pd.DataFrame(data_json["data"]), ignore_index=True)
    return big_df

def stock_us_spot_updated():
    big_df = pd.DataFrame()
    page_count = get_us_page_count()
    #page_count = 5
    #page_count = 1
    for page in range(1, page_count+1):
        # page = "1"
        #print("正在抓取第{}页的美股数据".format(page))
        us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
        js_code = execjs.compile(js_hash_text)
        dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
        us_sina_stock_dict_payload.update({"page": "{}".format(page)})
        print(us_sina_stock_dict_payload)
        res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
        data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
        updated_df = pd.DataFrame(data_json["data"])
        updated_df['page'] = page
        big_df = big_df.append(updated_df, ignore_index=True)
    return big_df

def get_stock_us_page(page):
    #print("正在抓取第{}页的美股数据".format(page))
    us_js_decode = "US_CategoryService.getList?page={}&num=20&sort=&asc=0&market=&id=".format(page)
    js_code = execjs.compile(js_hash_text)
    dict_list = js_code.call('d', us_js_decode)  # 执行js解密代码
    us_sina_stock_dict_payload.update({"page": "{}".format(page)})
    #print(us_sina_stock_dict_payload)
    res = requests.get(us_sina_stock_list_url.format(dict_list), params=us_sina_stock_dict_payload)
    data_json = json.loads(res.text[res.text.find("({") + 1: res.text.rfind(");")])
    return data_json["data"]

def stock_us_daily(symbol="BRK.A", factor=""):
    res = requests.get(us_sina_stock_hist_url.format(symbol))
    js_code = execjs.compile(hk_js_decode)
    dict_list = js_code.call('d', res.text.split("=")[1].split(";")[0].replace('"', ""))  # 执行js解密代码
    data_df = pd.DataFrame(dict_list)
    data_df["date"] = data_df["date"].str.split("T", expand=True).iloc[:, 0]
    data_df.index = pd.to_datetime(data_df["date"])
    del data_df["date"]
    data_df.astype("float")
    res = requests.get(us_sina_stock_hist_qfq_url.format(symbol))
    pdb.set_trace()
    qfq_factor_df = pd.DataFrame(eval(res.text.split("=")[1].split("\n")[0])['data'])
    #qfq_factor_df.columns = ["date", "qfq_factor"]
    if factor == "qfq":
        return qfq_factor_df
    else:
        return data_df


if __name__ == "__main__":
    df = stock_us_spot_updated()
    #print(df)
    df.to_csv("us_stock_list1.csv")
    #df = stock_us_daily(symbol="AMZN", factor="qfq")
    #print(df)

"""
if __name__ == "__main__":
    new_df = pd.DataFrame()
    count = 0
    while count < 20:
        count = count + 1
        time.sleep(10)
        df = stock_us_spot()
        pdb.set_trace()
        if not new_df.empty:
            new_df = pd.concat([new_df, df.loc[0:2]])
        else:
            new_df = df.loc[0:2]
        print(new_df)

    new_df.to_csv("realtime1.csv")
    #df = stock_us_daily(symbol="AMZN", factor="qfq")
    #print(df)
"""