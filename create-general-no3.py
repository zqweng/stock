import pandas as pd
import tushare as ts
import os
import pdb

root_dir = 'c:\\work\\stockdata\\'

if not os.path.exists(root_dir):
    os.mkdir(root_dir)
os.chdir(root_dir)

if not os.path.isfile('basic-no3.csv'):
    print('股票清单 not exist, create one')
    df = ts.get_stock_basics()
    df.to_csv('basic.csv')
    new_df = df[~df['code'].str.startswith('300')]
    new_df.to_csv('basic-no3.csv')
    index = new_df.index
else:
    print('股票清单 exists, load it')
    df = pd.read_csv('basic-no3.csv', converters={'code': lambda x: str(x)})
    index = df['code']

for stock_code in index[0:10]:
    print('index is ', stock_code)
    if not os.path.exists(root_dir + stock_code):
        os.mkdir(root_dir + stock_code)
        print('Directory', stock_code, 'Created')
    else:
        print('Directory', stock_code, ' already exists')

    os.chdir(root_dir + stock_code)
    stock_df = ts.get_hist_data(stock_code,start='2019-07-08')#,end='2019-01-09')
    if stock_df is None:
        print('fail get history file', stock_code)
        continue
    #print('successfully get history data for ', stock_code)
    stock_df.to_csv(stock_code + '.csv')

    for date_val in stock_df.index:
        #print ('date is ', date_val)
        if os.path.exists(date_val + '.csv'):
            print('date file ', date_val, ' exists for ', stock_code)
            #we assume if a file for a date exist, then all files before that date exist.
            break
        tick_df = ts.get_tick_data(stock_code,date=date_val,src='tt')

        if tick_df is None:
            print('history data on date ', date_val, 'for stock', stock_code, 'failed to retrieve')
            continue
        tick_df.to_csv(date_val + '.csv')    
    
        
    
    
