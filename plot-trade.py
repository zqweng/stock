import pandas as pd
import baostock as bs
import pdb
import datetime
import stock_library3 as mylib3
from mpl_finance import candlestick2_ohlc
import matplotlib as mpl
import matplotlib.pyplot as plt
import io
import random
import plot


def get_plot_figure_buf(df, subtitle):
    mpl.use('TkAgg')
    # plt.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams["figure.figsize"] = [9.6, 7.2]
    # fig=plt.figure(figsize=(20,10))
    fig = plt.figure()

    ax_price = plt.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=8)
    ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)

    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 8)
    # ax_price.xaxis.set_major_locator(mondays)
    # ax_price.xaxis.set_minor_locator(alldays)
    # ax_price.xaxis.set_major_formatter(weekFormatter)
    # ax_price.xaxis.set_minor_formatter(dayFormatter)
    # plot_day_summary(ax_price, quotes, ticksize=3)
    candlestick2_ohlc(ax_price, df['open'], df['high'], df['low'], df['close'], width=0.6)
    ax_price.plot(df["ma5"], "k", label="ma5", linewidth=0.5)
    ax_price.plot(df["ma10"], "y", label="ma10", linewidth=0.5)
    ax_price.plot(df["ma20"], "r", label="ma20", linewidth=0.5)
    ax_price.plot(df["upper"], "b--", label="upper", linewidth=0.5)
    ax_price.plot(df["lower"], "b--", label="upper", linewidth=0.5)
    # bar_x_pos = np.arange(len(df.index))
    ax_vol.bar(df.index, df["volume"])
    # ax_price.xaxis_date()
    # ax_price.autoscale_view()
    # plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    # pdb.set_trace()
    fig.suptitle(subtitle, fontsize=16)
    #print("y = {}".format(y))
    #ax_price.annotate('交易', xy=(x, y), xytext=(x, y * 1.02), arrowprops=dict(facecolor='blue', width=0.1, headwidth=7, shrink=0.05),)
    plt.show()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    plt.close(fig)
    return buf


def get_plot_figure_buf_bak(df, subtitle, x, y):
    mpl.use('TkAgg')
    # plt.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams["figure.figsize"] = [9.6, 7.2]
    # fig=plt.figure(figsize=(20,10))
    fig = plt.figure()

    ax_price = plt.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=8)
    ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)

    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 8)
    # ax_price.xaxis.set_major_locator(mondays)
    # ax_price.xaxis.set_minor_locator(alldays)
    # ax_price.xaxis.set_major_formatter(weekFormatter)
    # ax_price.xaxis.set_minor_formatter(dayFormatter)
    # plot_day_summary(ax_price, quotes, ticksize=3)
    candlestick2_ohlc(ax_price, df['open'], df['high'], df['low'], df['close'], width=0.6)
    ax_price.plot(df["ma5"], "k", label="ma5", linewidth=0.5)
    ax_price.plot(df["ma10"], "y", label="ma10", linewidth=0.5)
    ax_price.plot(df["ma20"], "r", label="ma20", linewidth=0.5)
    ax_price.plot(df["upper"], "b--", label="upper", linewidth=0.5)
    ax_price.plot(df["lower"], "b--", label="upper", linewidth=0.5)
    # bar_x_pos = np.arange(len(df.index))
    ax_vol.bar(df.index, df["volume"])
    # ax_price.xaxis_date()
    # ax_price.autoscale_view()
    # plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    # pdb.set_trace()
    fig.suptitle(subtitle, fontsize=16)
    print("y = {}".format(y))
    ax_price.annotate('交易', xy=(x, y*1.01), xytext=(x, y * 1.02), arrowprops=dict(facecolor='blue', width=0.1, headwidth=10, shrink=0.05),)
    #plt.show()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    fig.savefig("{}.png".format(random.randint(0, 1000)))
    buf.seek(0)

    plt.close(fig)
    return buf


"""
(Pdb) df.columns
Index(['证券代码', '证券名称', '成交日期', '成交时间', '买卖标志', '成交价格', '成交数量', '成交金额', '成交编号',
       '委托编号', '股东代码'],

Generally, double quotes are used for string representation and single quotes are used for regular expressions,
       
"""

def create_df_from_bao_rs_min(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    df_result = pd.DataFrame(data_list, columns=rs.fields)
    df_result = df_result.loc[df_result['volume'] != '0']
    if len(df_result.index) == 0:
        return None

    #df_result = df_result[['date', 'time', 'open', 'high', 'low', 'close', 'volume']]
    #df_result.set_index(['date', 'time'], inplace=True)
    #df_result.sort_index(ascending=False, inplace=True)
    #df_result = df_result.rename(columns={"volume": "amount"})
    return df_result


def plot_and_email_trade(df_trade):
    for i in df_trade.index:
        date_str = df_trade["成交日期"][i]
        time_str = df_trade["成交时间"][i]
        stock_code = df_trade["证券代码"][i]
        stock_code = "sh." + stock_code if stock_code[0] == "6" else "sz." + stock_code

        year, month, day = list(map(int, [date_str[0:4], date_str[4:6], date_str[6:8]]))
        time_list = list(map(int, time_str.split(":")))
        hour, minute, second = time_list[0], time_list[1], time_list[2]
        trade_date = datetime.datetime(year, month, day)

        if trade_date.weekday() == 0:
            start_date = (trade_date - pd.to_timedelta('4 days')).strftime('%Y-%m-%d')
            end_date = (trade_date + pd.to_timedelta('2 days')).strftime('%Y-%m-%d')
        elif trade_date.weekday() == 4:
            start_date = (trade_date - pd.to_timedelta('2 days')).strftime('%Y-%m-%d')
            end_date = (trade_date + pd.to_timedelta('4 days')).strftime('%Y-%m-%d')
        else:
            start_date = (trade_date - pd.to_timedelta('2 days')).strftime('%Y-%m-%d')
            end_date = (trade_date + pd.to_timedelta('2 days')).strftime('%Y-%m-%d')

        trade_datetime = datetime.datetime(year, month, day, hour, minute, second)
        subtitile = " {} {} {} {} 成交价格:{} 成交数量:{} 成交金额:{}".format(
            df_trade["证券代码"][i], df_trade["证券名称"][i], trade_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            df_trade["买卖标志"][i], df_trade["成交价格"][i], df_trade["成交数量"][i], df_trade["成交金额"][i]
        )

        second = 0

        if hour == 9 and minute == 25:
            minute1 = 35
        else:
            floor = minute // 10
            mod = minute % 10

            if mod < 5:
                minute1 = floor * 10 + 5
            else:
                minute1 = (floor + 1) * 10
                if minute1 == 60:
                    minute1 = 0
                    hour = hour + 1

        trade_datetime_updated = datetime.datetime(year, month, day, hour, minute1, second)

        rs = bs.query_history_k_data_plus(stock_code,
                                          "date,time,code,open,high,low,close,volume",
                                          start_date=start_date,
                                          end_date=end_date,
                                          frequency='5', adjustflag="2")
        df_result = create_df_from_bao_rs_min(rs)
        df_result = mylib3.ma(df_result)
        df_result = mylib3.boll(df_result)
        df_result = df_result.sort_index(ascending=True)

        str = trade_datetime_updated.strftime("%Y%m%d%H%M%S") + "000"
        df1 = df_result[df_result["time"] == str]

        get_plot_figure_buf_bak(df_result, subtitile, df1.index[0], df_trade["成交价格"][i])
        # get_plot_figure_buf(df_result, subtitile)


def plot_trade_and_save():
    df = pd.read_excel("2020-trade.xlsx", converters={'成交日期': lambda x: str(x), "证券代码": lambda x: str(x)})
    df_buy = df[df["买卖标志"] == "买入"]

    lg = bs.login()
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    plot_and_email_trade(df_buy)








