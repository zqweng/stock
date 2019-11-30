import baostock as bs
import pandas as pd
import numpy as np
import talib as ta
import datetime
import pdb
# 获取历史行情数据，并根据日K线数据设置警示价格
def return_constraintdict(stockcodelist):
    login_result = bs.login(user_id='anonymous', password='123456')
    print('login respond error_msg:'+login_result.error_msg)
    startdate = '2018-01-01'
    today = datetime.datetime.now()
    # A timedelta object represents a duration, the difference between two dates or times.
    delta = datetime.timedelta(days=1)

    # 获取截至上一个交易日的历史行情
    '''
    timespan = now - past
    #这会得到一个负数
    past - now
    attrs = [
    ("days","日"),( 'seconds',"秒"),( 'microseconds',"毫秒")
    #('min',"最小"),( 'max',"最大"),
    请注意它的参数顺序
    timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    timespan = timedelta(days=1)
    now - timespan #返回的是datetime型
    '''
    predate = today - delta
    '''
    # Formatting datetime
    >>> dt.strftime("%A, %d. %B %Y %I:%M%p") -> 'Tuesday, 21. November 2006 04:30PM'
    '''
    strpredate = datetime.datetime.strftime(predate, '%Y-%m-%d')
    for stockcode in stockcodelist:
        ### 获取沪深A股行情和估值指标(日频)数据并返回收盘价20日均线 ####
        # date 日期
        # code 股票代码
        # close 收盘价
        # preclose 前收盘价
        # volume 交易量
        # amount 交易额
        # adjustflag 复权类型
        # turn 换手率
        # tradestatus 交易状态
        # pctChg 涨跌幅
        # peTTM 动态市盈率
        # psTTM 市销率
        # pcfNcfTTM 市现率
        # pbMRQ 市净率
        '''
        首先下载股票上一个交易日之前的日K线行情数据.
        '''
        rs = bs.query_history_k_data("%s" % stockcode,
                                     "date,code,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                                     start_date=startdate,
                                     end_date=strpredate,
                                     frequency="d", adjustflag="2")
        print('错误报告：query_history_k_data respond error_code:' + rs.error_code)
        print('错误报告：query_history_k_data respond error_msg:' + rs.error_msg)
        #### 打印结果集 ####
        result_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            result_list.append(rs.get_row_data())
        #盯盘
        result = pd.DataFrame(result_list, columns=rs.fields)
        closelist = list(result['close'])
        closelist = [float(price) for price in closelist]
        print (closelist)

    '''
    然后计算上一交易日的20日均线，然后比较上一交易日20日均线的值和过去10天最高收盘价两个值，
    取其中的最大值作为阻力线.
    '''
    # 调用TA-Lib中的MA函数，计算20日均线值
    malist = ta.MA(np.array(closelist), timeperiod=20)
    print ('股票代码=%s，'%(stockcode,))
    if len(malist) > 20 and closelist[-20] > 0:
        ma20value = malist[-1]
        summit20day = max(closelist[-10:])
        # 以突破10日高点且在20日均线以上作为买入条件
        resistancelinedict[stockcode] = max(ma20value, summit20day)
    else:
        resistancelinedict[stockcode] = float(closelist[-1])

    bs.logout()
    return resistancelinedict


# 每次收到实时行情后，回调此方法
def callbackFunc(ResultData):
    # print(ResultData.data)
    for key in ResultData.data:
        # 当盘中价格高于警示价格，输出提示信息。
        '''
        然后再获取当日实时数据，如果某个时刻突破了这个阻力线，则发出提示信息。
         '''
        if key in resistancelinedict and float(ResultData.data[key][6]) > resistancelinedict[key]:
            print("%s,突破阻力线，可以买入" % key)

def test_real_time_stock_price(stockcode):
    login_result = bs.login_real_time(user_id='anonymous', password='123456')
    # 订阅
    rs = bs.subscribe_by_code(stockcode, 0, callbackFunc, "", "user_params")
    # rs = bs.subscribe_by_code("sz.300009", 0, callbackFunc, "", "user_params")
    if rs.error_code != '0':
        print("request real time error", rs.error_msg)
    else:
        # 使主程序不再向下执行。使用time.sleep()等方法也可以
        text = input("实时数据接收成功！ press any key to cancel real time \r\n")
        # 取消订阅
        cancel_rs = bs.cancel_subscribe(rs.serial_id)
    # 登出
    login_result = bs.logout_real_time("anonymous")

if __name__ == '__main__':
    resistancelinedict = {}
    # 自定义股票池
    stockcodelist = ['sz.000001']
    #stockcodelist = ['sh.600000', 'sz.300009', 'sz.300128',
    # 'sh.603568', 'sz.000049', 'sh.600518', 'sz.300532', 'sz.000001']
    stockcodes = ""
    for stockcode in stockcodelist:
        stockcodes = "%s%s," % (stockcodes, stockcode)
        stockcodes = stockcodes[:-1]
        print(stockcodes)

    #均线突破类型
    resistancelinedict = return_constraintdict(stockcodelist)
    #### 登出系统 ####
    test_real_time_stock_price(stockcodes)