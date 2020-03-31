
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick2_ohlc
import pdb
import api as myapi

def plot(df, period, info, prefix=""):
    mpl.use('TkAgg')
    #plt.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    #plt.rcParams["figure.figsize"] = [9.6, 7.2]
    #fig=plt.figure(figsize=(20,10))
    fig = plt.figure()

    ax_price = plt.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=8)
    ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)

    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 8)
    #ax_price.xaxis.set_major_locator(mondays)
    #ax_price.xaxis.set_minor_locator(alldays)
    #ax_price.xaxis.set_major_formatter(weekFormatter)
    #ax_price.xaxis.set_minor_formatter(dayFormatter)
    # plot_day_summary(ax_price, quotes, ticksize=3)
    candlestick2_ohlc(ax_price, df['open'], df['high'], df['low'], df['close'], width=0.6)
    ax_price.plot(df["ma5"], "k", label="ma5", linewidth=0.5)
    ax_price.plot(df["ma10"], "y", label="ma10", linewidth=0.5)
    ax_price.plot(df["ma20"], "r", label="ma20", linewidth=0.5)
    ax_price.plot(df["upper"], "b--", label="upper", linewidth=0.5)
    ax_price.plot(df["lower"], "b--", label="upper", linewidth=0.5)

    #bar_x_pos = np.arange(len(df.index))
    ax_vol.bar(df.index, df["volume"])
    #ax_price.xaxis_date()
    #ax_price.autoscale_view()
    #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    #pdb.set_trace()
    fig.suptitle('{} {} {} 流通{}亿股'.format(info.industry, info[0], info.code, info.outstanding), fontsize=16)
    #plt.show()
    fig.savefig(r"image\{}\{}{}.png".format(period, prefix, info.code))
    plt.close(fig)

def start_plot(period_type, stock_list, prefix=""):
    df_list = myapi.read_csv("basic-no3.csv")
    df_list["code"] = df_list.index
    count = 0
    for code in stock_list:
            count = count + 1
            df = pd.read_csv("C:\\Users\\johnny\\stockdata-bao\\{}\\{}.csv".format(period_type, code), nrows=100)
            df = df.iloc[::-1]
            df = df.reset_index()

            if code not in df_list.index:
                print("{} is not an valid code".format(code))
                continue
            df_info = df_list.loc[code]
            plot(df, period_type, df_info, "{}-{}-".format(prefix, count))

def get_code_list(list_file):
    df = myapi.read_csv(list_file)
    return df.index.to_list()

if __name__ == "__main__":
    prefix="bull"
    eex_li = ["002328"]
    bull_li= ["603005", "603026", "000818", "002605", "002185", "002837", "603986", "603068", "603936", "603938"]
    ex_li = ["002328", "002258", "603839", "002002", "603920", "002688", "002373", "002237", "002829", "600267",
             "002756",
             "002803", "603583", "002383", "002180", "002527"]
    week_list=["000700", "002837", "603138", "002623"]
    week_list_new= ['000078', '000518', '000652', '000955', '002214', '002219', '002301',
       '002326', '002467', '002551', '002693', '002838', '600200', '600222',
       '600513', '600661', '600664', '600789', '600866', '603238', '603301',
       '603456', '603601', '603726', '603880']
    week_list_610 = ['000716', '000998', '002385', '600053', '603366', '603598', '603721', '000927', '000955',
                     '002261', '002291', '603598', '000026', '002291', '002623', '600695', '601700', '601990', '600712']
    #start_plot("60", week_list_610, "week_610_")
    #start_plot("day", week_list_610, "week_610_")
    #start_plot("15", week_list_610, "week_610_")
    #start_plot("week", week_list_610, "week_610_")
    mylist = get_code_list(r"result\ma20-up.csv")
    #mylist = get_code_list(r"mystocklist-detail.csv")
    start_plot("day", mylist, "ma20-")
    #start_plot("60", mylist, "ma20-up")

