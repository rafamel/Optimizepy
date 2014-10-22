import numpy as np
import pandas as pd
import datetime as dt
import math
import time


import Quandl


# INPUT QUANDL API KEY HERE
qdl_apikey = ""


def get_data(symbols, exchange, dt_start = None, dt_end = None):
    ''' symbols = List of currencies. Ex. ['EURUSD', 'EURCAD'] '''
    
    # Check for API key
    if qdl_apikey == "":
        print 'IMPORTANT: No Quandl API key has been provided. No more than 50 requests will be allowed.'
        raw_input('Press enter to continue... ')
        print
        
    # 1. Formatting start and end dates/days to access Quandl API
    if dt_start != None:
        dt_start = dt_start.strftime('%Y-%m-%d')
    if dt_end != None:
        dt_end = dt_end.strftime('%Y-%m-%d')
    
    # 2. Formatting pairs (symbols) from 'EURUSD' to 'QUANDL/EURUSD.1' (the .1 to only get the second column of data)
    
    #Forex
    if exchange == 'custom':
        prefix = ''
        sufix_column = ''
    elif exchange == 'fx':
        prefix = 'QUANDL/'
        sufix_column = '.1'
    #Madrid
    elif exchange == 'mc':
        prefix = 'YAHOO/MC_'
        sufix_column = '.4'
    #NASDAQ
    elif exchange == 'nasdaq':
        prefix = 'GOOG/NASDAQ_'
        sufix_column = '.4'
    else:
        raise Exception("No valid exchange/market entered.")
    
    
    mod_symbols = symbols[:]   
    
    for i in range(len(symbols)):
        mod_symbols[i] = prefix+str(symbols[i])+sufix_column
    
    quandl_data = Quandl.get(mod_symbols, collapse="daily", trim_start=dt_start, trim_end=dt_end, authtoken=qdl_apikey)

    #Needed to save dates in dataframe
    quandl_data = quandl_data.reset_index()
    
    # Checking none of the columns is empty (error in symbols)
    i_num = 0
    for q_num in quandl_data.iloc[-1,1:]:
        if math.isnan(q_num):
            raise Exception("There was an error getting symbols data. No data received for "+symbols[i_num])
        i_num += 1
    
    #Filling nans
    pd_quandl_data = pd.DataFrame(quandl_data.iloc[:,1:])
    pd_quandl_data = pd_quandl_data.fillna(method='ffill')
    pd_quandl_data = pd_quandl_data.fillna(method='bfill')
    pd_quandl_data = pd_quandl_data.fillna(1.0)
    quandl_data.iloc[:,1:] = pd_quandl_data
    
    #Columns to original symbols
    quandl_data.columns = ['Date']+symbols
    
    # Return as np array because it's what the rest of the system expect. This should be changed to maintain the Pandas Dataframe.
    quandl_data = np.asarray(quandl_data)
    
    return quandl_data



# EXAMPLE CALL

#symbols = ['EURUSD', 'EURCAD']
#exchange = 'fx'
#dt_start = dt.datetime(2011, 1, 1)
#dt_end = dt.datetime(2011, 12, 31)


#print get_data(symbols, exchange, dt_start, dt_end)
