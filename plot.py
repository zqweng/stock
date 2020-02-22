
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick2_ohlc
import pdb
import api as myapi

def plot(df, period, info):
    mpl.use('TkAgg')
    #plt.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 8)
    #ax.xaxis.set_major_locator(mondays)
    #ax.xaxis.set_minor_locator(alldays)
    #ax.xaxis.set_major_formatter(weekFormatter)
    #ax.xaxis.set_minor_formatter(dayFormatter)

    # plot_day_summary(ax, quotes, ticksize=3)
    candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.6)

    #ax.xaxis_date()
    #ax.autoscale_view()
    #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    #pdb.set_trace()
    fig.suptitle('{} {}'.format(info[0], info.code), fontsize=16)
    fig.savefig(r"image\{}\{}.png".format(period, info.code))
    plt.close(fig)


if __name__ == "__main__":
    ex_li = ["002328", "002258", "603839", "002002", "603920", "002688", "002373", "002237", "002829", "600267",
             "002756",
             "002803", "603583", "002383", "002180", "002527"]
    df_list = myapi.read_csv("basic-no3.csv")
    df_list["code"] = df_list.index
    for period_type in ["day", "15"]:
        for code in ex_li:
            df = pd.read_csv("C:\\Users\\johnny\\stockdata-bao\\{}\\{}.csv".format(period_type, code), nrows=120)
            df = df.iloc[::-1]

            if code not in df_list.index:
                print("{} is not an valid code".format(code))
                continue
            df_info = df_list.loc[code]
            plot(df, period_type, df_info)