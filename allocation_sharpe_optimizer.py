import datetime as dt
import numpy as np

import simulate_portfolio_allocation as smlt
import all_permutes as permutes
import get_data

def allocation_op(symbols, exchange, allow_short, days = None, filter_symbols = 5, data_allocate = None, dt_start = None, dt_end = None):
    ''' Function ALLOCATION / SHARPE RATION OPTIMIZER
    Tests all possible portfolio allocations for **symbols** and determines which one had the **best Sharpe ratio** for the period [today - *days*] to today _or_ from *dt_start* to *dt_end*.
    days = days backwards from today. It will measure *real* days, not just trading days.
    dt_start and dt_days = dates (from) and (to). It will measure trading days. Alternative to "days".
    na_price = array of prices for the symbols, including a first column with dates. Optional.
    allow_short = Is going short allowed in the model?
    filter_symbols = (int) calculate the sharpe ratio for all symbols inputed
        and only choose and try different allocations for those with the highest
        sharpe. 0 to deactivate.    '''
    
    # I'll copy symbols because manipulating it for some reason changes its value for higher scopes as backtester ???
    symbols_op = symbols[:]
    
    # 0. Start and End dates from range of days
    if days == None and (dt_start == None or dt_end == None):
        raise Exception("Either (days) or (dt_start and dt_end) must be inputed.")
    elif days != None:
        dt_end = dt.datetime.now()
        dt_start = dt_end-dt.timedelta(days)
    else:
        days = (dt_end-dt_start).days
    

    # 1. Get data, if needed
    if data_allocate == None:
        data_allocate = get_data.get_data(symbols, exchange, dt_start, dt_end)
        
        
    # 2. Flip symbols & na_price if needed

    flip_symbols = symbols[:]
    if allow_short == 1:
        long_or_short = data_allocate[-1,1:] / data_allocate[0,1:]
        for i in range(len(long_or_short)):
            if long_or_short[i] < 1:
                data_allocate[:,i+1] = np.flipud(data_allocate[:,i+1])
                flip_symbols[i] = '-'+flip_symbols[i]
                
                
    # 3. Filter symbols, if needed, copy values and assign corresponding length to matrix
    print
    
    if filter_symbols == 0 or len(symbols) <= filter_symbols:
        na_price_chosen = data_allocate
        permutes_length = len(symbols_op)
        filter_chosen = range(len(symbols_op)+1)
    else:
        permutes_length = filter_symbols
        
        print 'Pre-filtering symbols...'
        print
        
        filter_sharpe = np.array([])
        for i in range(len(symbols_op)):
            this_allocation = np.zeros(len(symbols_op))
            this_allocation[i] = 1.0
            get_sharpe, get_returns = smlt.simulate(data_allocate[:,1:], dt_start, dt_end, symbols_op, this_allocation)
            filter_sharpe = np.insert(filter_sharpe, len(filter_sharpe), get_sharpe)
        
        filter_chosen = np.array([])
        for i in range(filter_symbols):
            chosen_sym_idx = np.argmax(filter_sharpe)
            filter_chosen = np.insert(filter_chosen, len(filter_chosen), chosen_sym_idx, axis=0)
            filter_sharpe[chosen_sym_idx] = 0
        
        # Select symbols
        filter_chosen = filter_chosen.astype(int)
        symbols_op = list(np.array(symbols_op)[filter_chosen])
        flip_symbols = list(np.array(flip_symbols)[filter_chosen])
        
        # Select columns from na_price and also column 0 (dates)
        filter_chosen += 1
        filter_chosen = np.insert(filter_chosen, 0, 0, axis=0)
        na_price_chosen = data_allocate[:,filter_chosen]
                    
    
    # 4. Create a matrix for all possible allocations that sum up to 1
    # with 0.1 steps
    print
    matrix = permutes.permutes_f(0.1, permutes_length)
    print
    
    # 5. Simulate Sharpe ratio for each allocation
    
    num_rows = len(matrix[:,0])
    max_sharpe = 0.0
    
    print 'Computing allocations ('+str(num_rows)+' left)...'
    print
    
    max_sharpe = 0
    max_returns = 0
    for i in range(num_rows):
        # Print indicator of progress each 5 computations
        if i%5 == 0:
            print i,'of',num_rows

        this_allocation = np.array(matrix[i,:])
        
        get_sharpe, get_returns = smlt.simulate(na_price_chosen[:,1:], dt_start, dt_end, symbols_op, this_allocation)
        
        # If this sharpe is better than the one saved, then save this one instead
        if get_sharpe > max_sharpe:
            max_sharpe = get_sharpe
            max_returns = get_returns
            best_allocation = matrix[i,:]
            print
            print '-------------------------------------'
            print
            print 'BETTER ALLOCATION FOUND'
            print 'Sharpe ratio:',get_sharpe
            print
            print flip_symbols
            print this_allocation
            print
            print '-------------------------------------'
            print
            
    print
    print '-------------------------------------'
    print
    
    
    
    
    # If the best allocation loses money, then don't invest in anything
    if max_returns <= 1 or max_sharpe <= 0:
        max_returns = 1
        trading_days = ((dt_end-dt_start).days * 252) / 365
        max_sharpe = 1 * np.sqrt(trading_days)
        best_allocation = np.zeros(len(symbols_op))
        
        
    time_n = dt.datetime.now().strftime('%Y-%m-%d')
    
    one = 'For a '+str(days)+' days period ('+str(time_n)+'):'
    two = '-------------------------------------'
    three = 'Symbols (minus sign = going short): '+str(flip_symbols)
    four = 'Best allocation: '+str(best_allocation)
    five = 'Max sharpe: '+str(max_sharpe)
    six = 'Cumulative returns: '+str((max_returns-1)*100)+'% ('+str(days)+' days period)'
    
    print one
    print two
    print three
    print four
    print five
    print six
    
    #SAVE FILE
    #filename = time_n+'.'+dt.datetime.now().strftime('%H%M%S%f')+'.txt'
    #save = one+'\r\n '+two+'\r\n '+three+'\r\n '+four+'\r\n '+five+'\r\n '+six+'\r\n'
    #text_file = open(filename, "w")
    #text_file.write(save)
    #text_file.close()

    
    best_allocation = list(best_allocation)
    return best_allocation, flip_symbols, filter_chosen






# Call function example
# DEPRECATED

#dt_start = dt.datetime(2011, 1, 1)
#dt_end = dt.datetime(2011, 12, 31)
#symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']

#dt_start = dt.datetime(2010, 1, 1)
#dt_end = dt.datetime(2010, 12, 31)
#symbols = ['BRCM', 'TXN', 'AMD', 'ADI']

#dt_start = dt.datetime(2011, 1, 1)
#dt_end = dt.datetime(2011, 12, 31)
#symbols = ['BRCM', 'ADBE', 'AMD', 'ADI']


#exchange = 'fx'
#days = 30
#symbols = ['EURUSD', 'EURGBP', 'EURCHF', 'EURCAD', 'EURJPY']
#allow_short = 1


#exchange = 'fx'
#days = 30
#symbols = ['EURUSD', 'EURGBP', 'EURCHF', 'EURCAD', 'EURJPY']
#allow_short = 1
#filter_symbols = 3

#allocation_op(symbols, exchange, allow_short, days, filter_symbols)

