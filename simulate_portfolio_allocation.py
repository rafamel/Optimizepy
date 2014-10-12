import datetime as dt
import numpy as np
import math


def simulate(na_price_nodate, dt_start, dt_end, symbols, portf_allocation):
    ''' Simulate a Portfolio Allocation Function
    Returns sharpe ratio and cumulative returns
    na_price_nodate = np.array of data without column 0 of dates
    symbols = if any of them is negative, it will flip the column'''
    
    
    # 1. Get closing prices for each day for the selected 

    ## STEP 1: CUMULATIVE RETURN

    for i in range(len(symbols)):
        if symbols[i][0] == '-':
            na_price_nodate[:,i] = np.flipud(na_price_nodate[:,i])
            
    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price_nodate / na_price_nodate[0, :]
    na_normalized_price = na_normalized_price * portf_allocation
    
    cum_ret = np.nansum(na_normalized_price[-1]) / np.nansum(na_normalized_price[0])
    #print 'Cumulative returns:',cum_ret
    
    ## STEP 2: AVERAGE DAILY RETURN
    one_row = np.nansum(na_normalized_price, axis=1)
    
    for i in range(len(one_row)-1, 0, -1):
        one_row[i] = (one_row[i] / one_row[i-1]) - 1
    one_row[0] = 0
    
    av_day = np.mean(one_row)
    #print 'Average:',av_day
    
    ## STEP 3: STANDARD DEVIATION

    std_day = np.std(one_row)
    #print 'STD:',std_day

    ## STEP 4: SHARPE
    trading_days = ((dt_end-dt_start).days * 252) / 365
    sharpe_rt = (av_day / std_day) * np.sqrt(trading_days)
    if math.isnan(sharpe_rt):
        sharpe_rt = 0
    #print 'Sharpe:',sharpe_rt

    ## RETURNS SHARPE RATIO,  CUMULATIVE RETURNS, Symbols (some sign might be changed
    ## if going short was allowed)
    return sharpe_rt, cum_ret

    #print 'Cumulative returns:',cum_ret
    #print 'Average:',av_day
    #print 'STD:',std_day
    #print 'Sharpe:',sharpe_rt




    
# EXAMPLES
# _______________________________________

#symbols = ['EURCAD', 'EURGBP']
#portf_allocation = [0.5, 0.5]
#dt_start = dt.datetime(2011, 1, 1)
#dt_end = dt.datetime(2011, 12, 31)
#exchange = 'fx'
#import get_data
#na_price = get_data.get_data(symbols, exchange, dt_start, dt_end)

#dt_end = dt.datetime(2014, 10, 11)
#dt_start = dt_end-dt.timedelta(30)
#exchange = 'fx'
#portf_allocation = [0.2, 0.1, 0.7]
#symbols = ['EURGBP', 'EURUSD', 'EURCHF']
#import get_data
#na_price = get_data.get_data(symbols, exchange, dt_start, dt_end)
#symbols = ['-EURGBP', '-EURUSD', 'EURCHF']


#dt_start = dt.datetime(2000, 4, 14)
#dt_end = dt.datetime(2000, 5, 26)
#exchange = 'mc'
#portf_allocation = [0.20000000000000001, 0.59999999999999998, 0.10000000000000001, 0.0, 0.0, 0.10000000000000001]
#symbols = ['ABE', 'FCC', 'IBE', 'SAN', 'REP', 'TEF']
#import get_data
#na_price = get_data.get_data(symbols, exchange, dt_start, dt_end)
#symbols = ['-ABE', 'FCC', '-IBE', '-SAN', 'REP', '-TEF']


#dt_start = dt.datetime(2003, 3, 7)
#dt_end = dt.datetime(2003, 4, 18)
#exchange = 'mc'
#portf_allocation = [0.40000000000000002, 0.0, 0.29999999999999999, 0.20000000000000001, 0.0, 0.10000000000000001]
#symbols = ['ABE', 'FCC', 'IBE', 'SAN', 'REP', 'TEF']
#import get_data
#na_price = get_data.get_data(symbols, exchange, dt_start, dt_end)
#symbols = ['ABE', '-FCC', 'IBE', '-SAN', 'REP', '-TEF']


# Call function
#a, b = simulate(na_price[:,1:], dt_start, dt_end, symbols, portf_allocation)
#print 'Sharpe:', a
#print 'Returns:', b
