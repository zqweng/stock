# -*- coding: utf-8 -*-
import pandas as pd
import baostock as bs
from pathlib import Path
import platform
import pdb
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import os

def send_email(topic="", content=""):
    # me == my email address
    # you == recipient's email address
    me = "johnny.weng8@gmail.com"
    you = "johnny.weng8@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = topic
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "org"
    html = """\
    <html>
    <head></head>
    <body>
        {}
        <p>Hi!<br>
        How are you html?<br>
        Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """.format(content)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login("johnny.weng8@gmail.com", "Weng0073") 
    
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    s.sendmail("johnny.weng8@gmail.com", "ruri299ceke@post.wordpress.com", msg.as_string())
    s.quit()


def email(df, subject="", to_addr="johnny.weng8@gmail.com", from_addr="johnny.weng8@gmail.com"):
    recipients = [to_addr]
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr

    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(df.to_html())

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.sendmail(msg['From'], emaillist, msg.as_string())

def read_csv(stock_list_file, local=False, market="China"):
    if not local and platform.system() == "Windows":
        file = Path("C:/Users/johnny/PycharmProjects/stock-github")/stock_list_file
    else:
        file = stock_list_file
    df = pd.read_csv(file, converters={'code': lambda x: str(x)})
    if market == "China":
        df.set_index('code', inplace=True)
    else:
        df.set_index('code', inplace=True)
    return df

def import_col(df_profit, df_info):
    df_profit["code"] = df_profit["code"].str.strip("szh.")
    df_profit = df_profit.set_index("code")

    df_profit = df_profit.drop(columns="profitForcastAbstract")

    df_profit = df_profit.reindex(columns=df_profit.columns.tolist() + ['name', 'industry', 'outstanding'])

    for code in df_profit.index:
        df_profit.loc[code, 'name'] = df_info.loc[code][0]
        df_profit.loc[code, 'industry'] = df_info.loc[code].industry
        df_profit.loc[code, 'outstanding'] = df_info.loc[code].outstanding

    return df_profit


def get_profit_forecast(start_date="2020-03-01", end_date="2020-12-31"):
    df_all = pd.DataFrame()

    df_orig = read_csv(r"/home/johnny/code/stock/basic-no3.csv")
    df_orig = df_orig[0:1000]
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    stock_list = df_orig.index.to_list()
    new_stock_list = ["sz.{}".format(code) if code[0] == '0' else "sh.{}".format(code) for code in stock_list]

    num = 0
    for code in new_stock_list:
        rs_forecast_list = []

        #### 获取公司业绩预告 ####
        rs_forecast = bs.query_forecast_report(code, start_date, end_date)
        print('query_forecast_reprot respond error_code: {} / {}'.format(rs_forecast.error_code, num))
        print('query_forecast_reprot respond  error_msg: {} / {}'.format(rs_forecast.error_msg, num))
        num = num + 1

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

    if df_all.empty:
        print("no forecast retrieved ")
        return df_all

    df1 = import_col(df_all, df_orig)
    df1 = df1[df1["profitForcastType"]=="预增"]
    df1 = df1.sort_values(by = "profitForcastExpPubDate")
    df1.to_csv(r"profit.csv")
    print(df1)
    #### 登出系统 ####
    bs.logout()
    return df1

if __name__ == "__main__":
    path = "/home/johnny/code/stock"
    os.chdir(path)

    df1 = get_profit_forecast()

    #email(df1, "profit")
    #df1 = read_csv("profit.csv")

    if not df1.empty:
        send_email(topic="profit-forecast", content=df1.to_html())
