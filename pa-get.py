# 获取所有上市公司简易财务报表从网易
import requests
from bs4 import BeautifulSoup
import pandas
import time

import pdb

res = requests.get("http://quotes.money.163.com/data/caibao/yjgl_ALL.html?reportdate=20200331")

soup = BeautifulSoup(res.content, features="lxml")

select = soup.select("#plate_performance")
select_str = str(select[0])
df = pandas.read_html(select_str)[0]

url = "http://quotes.money.163.com/data/caibao/yjgl_ALL.html?reportdate=20200331&sort=publishdate&order=desc&page="
for i in range(1,154):
    url_working = url + str(i)
    res = requests.get(url_working)
    soup = BeautifulSoup(res.content, features="lxml")
    select = soup.select("#plate_performance")
    select_str = str(select[0])
    df1 = pandas.read_html(select_str)[0]
    df = pandas.concat([df, df1], ignore_index=True)
    time.sleep(0.5)
    print(df1)

df.to_csv("2020-q1.csv")
