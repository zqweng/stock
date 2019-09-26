stock library:
resample function
day_lower_shadow_line:  check if there is a lower shadow line.
day_break_moving_avg:   check if price breakthrough ma5/ma10/ma20 in one day
day_k_cross:            check if ma5 cross ma10
day_n_days_small_up:    check if there are continually price day_n_days_small_up
day_find_up_period:     locate a period in days/hours/weeks of kindlestick that price up


stock library2:
find_ma5_up:            check if ma5 keeps going up and cross ma10 and ma20
find_ma10_up:           check if ma10 keeps going up
find_cross_ma20:        check if price drop bellow and then go up across ma20



买入点1：
1） day:
    ma5 > ma10: 5 days in a row
    ma5 rise 5days in a row
    ma10 rise 5 days in a row

2) week:
   ma10 rise two weeks in a row
   lowest price is above ma5 and ma10


how to unifiy the record format for day and week and month:

in current tushare, the fields in day file is:

date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20

in baostock, it supports

date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST

so the common fields are:
date,open,high,close,low,volume,price_change,p_change, (ma5, ma10, ma20)
ma5, ma10 and ma20 should be calculated by hand when loading data from baostock.

so when load data from baostock, first thing is to remove unwanted fields and rename pctChg to p_change
keep the old stockdata loaded from tushare, recreated a new database from baostock

create a function that find w shape in days record.
1: set date as index
1: find the lowest price in the given period. use pandas min() method
2: to the right, find a peak and a valley.
    to find a peak, in next five records, find the max and it is 15% up than the lowest, and it must be at least two records away.
    then find the lowest and it is at least 10% lower than the max,
    then to the right of the second minimum, all records are higher than this,
    to the left of the first minimum, all records are higher than this.


how to rank stock list:
two measurements: PE and total shares
weight of PE is 60
weight of share is 40
1/log10(pe) + 1/log10(share)

find pe = 0 and change it to 10000:

NO difference
df.loc[df['high']>29 ]
df[df['high']>29 ]

bind two search together:

1: update day records, at the end of month, update month
2: calculate history high and one year high, generate file in result folder
3: calculate w-shape, generate file in result folder
4: calculate ma5 across ma10


//  scale a column to a range. pandas array can be treated as a two d array, use to_numpy() to create such an array
df['p_change'] = MinMaxScaler().fit_transform(df[['p_change']].to_numpy())


对于一个DataFrame A，A.loc[k]是读取A中index为k的那一行。A.iloc[k]是读取A中的第k行。

MinMaxScaler
X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
X_scaled = X_std * (max - min) + min

one mistake easily made:
df.set_index('date'), do not set inplace=True
for row in df.itertuples:
    row.index = xxx,    should be row.Index this Index is the label of the element in tuples

dataframe idxmax():
Return index of first occurrence of maximum over requested axis

moving average calculate:
pandas rolling method, take a window size of k and perform mathematical operation on it
pd['close'].rolling(3).mean()

df_old = df[:-2].copy()
if you dont call copy(), df_old will have a copy flag internally, in the future if you want to make some changes on df_old, it will show a warning

reindex()
conform dataframe to new index with optional filling logic, placing NA/NaN in locations having no value in the previous index.

dataframe.dtypes
return a Series with the datatype of each column

如果不是主升浪，买股一定要在20日线附近买
不要买正在做顶的股票，
股票价格不能离60日太远，也不能离20日太远。主升浪除外。
离20日和60日的距离是根据股性来决定的。
