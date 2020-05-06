
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick2_ohlc
import pdb
import platform
from smtplib import SMTP
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import email.encoders as Encoders

import io

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

def get_email_mime(subject=""):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    
    # Define these once; use them twice!
    strFrom = 'johnny.weng8@gmail.com'
    strTo = 'johnny.weng8@gmail.com'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    return msgRoot, msgAlternative

def send_email_smtp(msgRoot):

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login("johnny.weng8@gmail.com", "Weng0073") 
    
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    s.sendmail("johnny.weng8@gmail.com", "ruri299ceke@post.wordpress.com", msgRoot.as_string())
    s.quit()


def send_email():
    
    msgRoot, msgAlternative = get_email_mime()


    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('day-my_day610_-1--000818.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<img src="cid:image2">', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('day-my_day610_-2--002603.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage)

    send_email_smtp(msgRoot)

def get_plot_figure_buf(df, subtitle):
    #mpl.use('TkAgg')
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
    fig.suptitle(subtitle, fontsize=16)
    #plt.show()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    
    plt.close(fig)
    return buf


def plot(df, period, info, prefix=""):
    mpl.use('TkAgg')

    plt.rcParams['font.sans-serif'] = ['SimHei']

    fig = plt.figure()

    #pdb.set_trace()
    ax_price = plt.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=8)
    ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)
    #ax_price = fig.subplots()

    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(10, 8)
    candlestick2_ohlc(ax_price, df['open'], df['high'], df['low'], df['close'], width=0.6)
    ax_price.plot(df["ma5"], "k", label="ma5", linewidth=0.5)
    ax_price.plot(df["ma10"], "y", label="ma10", linewidth=0.5)
    ax_price.plot(df["ma20"], "r", label="ma20", linewidth=0.5)
    ax_price.plot(df["upper"], "b--", label="upper", linewidth=0.5)
    ax_price.plot(df["lower"], "b--", label="upper", linewidth=0.5)

    ax_vol.bar(df.index, df["volume"])
    fig.suptitle('{} {} {} 流通{}亿股'.format(info.industry, info[0], info.code, info.outstanding), fontsize=16)
    plt.show()

def start_plot(period_type, stock_list, prefix=""):
    df_list = read_csv("basic-no3.csv")
    df_list["code"] = df_list.index
    count = 0
    for code in stock_list:
            count = count + 1
            if platform.system() == "Windows":
                file_name =  "C:\\Users\\johnny\\stockdata-bao\\{}\\{}.csv".format(period_type, code)
            else:
                file_name = "/home/johnny/stockdata-bao/{}/{}.csv".format(period_type, code)
            df = pd.read_csv(file_name, nrows=100)
            df = df.iloc[::-1]
            df = df.reset_index()

            if code not in df_list.index:
                print("{} is not an valid code".format(code))
                continue
            df_info = df_list.loc[code]
            plot(df, period_type, df_info, "{}-{}-".format(prefix, count))

def start_plot_save_in_email(msgRoot, msgAlternative, period_type, stock_list, prefix=""):
    df_list = read_csv("basic-no3.csv")
    count = 0
    for code in stock_list:
            count = count + 1

            if code not in df_list.index:
                print("{} is not an valid code".format(code))
                continue

            if platform.system() == "Windows":
                file_name = "C:\\Users\\johnny\\stockdata-bao\\{}\\{}.csv".format(period_type, code)
            else:
                file_name = "/home/johnny/stockdata-bao/{}/{}.csv".format(period_type, code)

            df = pd.read_csv(file_name, nrows=100)
            df = df.iloc[::-1]
            df = df.reset_index()

            code_info = df_list.loc[code]
            subtitle = '{} {} {} 流通{}亿股'.format(code_info.industry, code_info[0], code, code_info.outstanding)
            buf = get_plot_figure_buf(df, subtitle)

            # We reference the image in the IMG SRC attribute by the ID we give it below
            msgText = MIMEText(
                '图形如下[category profit forecast]<br><img src="cid:image{}"><br>'.format(count), 'html')
            msgAlternative.attach(msgText)

            part = MIMEBase('application', "octet-stream")
            part.set_payload(buf.read())
            Encoders.encode_base64(part)
            part.add_header('Content-ID', '<image{}>'.format(count))
            msgRoot.attach(part)
    
    return msgRoot


def get_code_list(list_file):
    df = myapi.read_csv(list_file)
    return df.index.to_list()

def plot_stock(stock_list, subject=""):
    prefix="bull"
    msgRoot, msgAlternative = get_email_mime(subject=subject)
    msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, subject,  stock_list, subject + "_")
    send_email_smtp(msgRoot)



def plot_stock_list(stock_list):
    frame_size = 25
    for x in range(0, len(stock_list), frame_size):

        msgRoot, msgAlternative = get_email_mime(subject="60 minutes K")
        msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "60", stock_list[x:x+frame_size], "my_60_")
        send_email_smtp(msgRoot)

        msgRoot, msgAlternative = get_email_mime(subject="Day K")
        msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "day", stock_list[x:x+frame_size], "my_day_")
        send_email_smtp(msgRoot)


if __name__ == "__main__":
    prefix="bull"
    my_current_list = ["000818", "002603", "002286", "000911", "000823", "002852", "603360","603859","601872"]
    #msgRoot, msgAlternative = get_email_mime(subject="60 minutes K")
    start_plot("60", my_current_list, "my_60_")
    #msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "day", my_current_list, "my_day610_")
    #msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "60", my_current_list, "my_60_")
    #start_plot("15", week_list_610, "week_610_")
    #start_plot("week", week_list_610, "week_610_")
    #mylist = get_code_list(r"result\ma20-up.csv")
    #mylist = get_code_list(r"mystocklist_detail.csv")
    #start_plot("day", mylist, "ma20-")
    #start_plot("60", mylist, "ma20-up")
    #send_email() 
    #send_email_smtp(msgRoot)

    #msgRoot, msgAlternative = get_email_mime(subject="Day K")
    #start_plot("60", my_current_list, "my_60_")
    #msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "day", my_current_list, "my_day_")
    #msgRoot = start_plot_save_in_email(msgRoot, msgAlternative, "60", my_current_list, "my_60_")
    #start_plot("15", week_list_610, "week_610_")
    #start_plot("week", week_list_610, "week_610_")
    #mylist = get_code_list(r"result\ma20-up.csv")
    #mylist = get_code_list(r"mystocklist_detail.csv")
    #start_plot("day", mylist, "ma20-")
    #start_plot("60", mylist, "ma20-up")
    #send_email() 
    #send_email_smtp(msgRoot)
