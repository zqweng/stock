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




