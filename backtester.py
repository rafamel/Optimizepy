import datetime as dt
import numpy as np
import sys

import get_data
import allocation_sharpe_optimizer
import simulate_portfolio_allocation as smlt
import all_permutes as permutes


#Allow to disable printing allocation_sharpe_optimizer
class NullDevice():
    def write(self, s):
        pass    
    
    
def backtester(symbols, exchange, allow_short, days_backwards, days_forward, filter_symbols = 5):
    ''' 
    filter_symbols = (int) calculate the sharpe ratio for all symbols inputed when
        running allocation_sharpe_optimizer and only choose and try different allocations for those with the highest
        sharpe. 0 to deactivate.
    '''

    print 'Starting backtest...'
    print
    
    # Do permutations before calling to allocation_sharpe_optimizer, which doesn't print anything into console
    if filter_symbols == 0 or len(symbols) <= filter_symbols:
        permutes_length = len(symbols)
    else:
        permutes_length = filter_symbols
    
    permutes.permutes_f(0.1, permutes_length)
    print
    
    # Get dates and prices for all dates
    print 'Getting data...'
    print
    all_data_price = get_data.get_data(symbols, exchange)
    print 'Done!'
    print
    
    n = 0
    for i in range(days_backwards-1, len(all_data_price[days_backwards-1:,0]), days_forward):
        

        dt_start = all_data_price[i-days_backwards+1,0]
        dt_end = all_data_price[i,0]
        
        # CALCULATE BEST ALLOCATION IN THE PAST
        #Disable printing
        original_stdout = sys.stdout
        sys.stdout = NullDevice()
        
        data_allocate = np.array(all_data_price[i-days_backwards+1:i+1])
        allocation, these_symbols, filter_chosen = allocation_sharpe_optimizer.allocation_op(symbols, exchange, allow_short, None, filter_symbols, data_allocate, dt_start, dt_end)
        #Enable printing again
        sys.stdout = original_stdout
        
        # CALCULATE HOW WELL WOULD IT HAVE DONE FORWARDS
        dt_start_forward = dt_end
        dt_end_forward = all_data_price[i+days_forward,0]
        
        
        if sum(allocation) == 0:
            trading_days = ((dt_end-dt_start).days * 252) / 365
            get_sharpe = 1 * np.sqrt(trading_days)
            get_returns = 1
        else:
            
            data_simulate = np.array(all_data_price[i:i+days_forward+1,filter_chosen])
            get_sharpe, get_returns = smlt.simulate(data_simulate[:,1:], dt_start_forward, dt_end_forward, these_symbols, allocation)
        
        # Returns are back in 1.XX format. Remove 1 and compute %
        get_returns = (get_returns-1)*100 
                
        if i == days_backwards-1:
            backtester_log = [['Cumulative return', 'Return', 'Sharpe', 'Optimization from', 'Optimization until/Invested from', 'Invested until']]
            cumulative_returns = get_returns
            dt_first_invested = all_data_price[i,0]
        else:
            cumulative_returns += get_returns
        
        
        progress_in_days = (dt_end_forward-dt_first_invested).days
        dt_start = dt_start.strftime('%Y-%m-%d')
        dt_end = dt_end.strftime('%Y-%m-%d')
        dt_end_forward = dt_end_forward.strftime('%Y-%m-%d')
        
        
        this_backtest = [cumulative_returns, get_returns, get_sharpe, dt_start, dt_end, dt_end_forward]
        backtester_log = np.insert(backtester_log, len(backtester_log), this_backtest, axis=0)
        
        print 'Invested in: '+str(these_symbols)
        print 'Allocation: '+str(allocation)
        print str(dt_end_forward)+' (year '+str(progress_in_days/365.0)+') cumulative return: '+str(cumulative_returns)+'%'
        print
        
        n += 1
        if n%10 == 0:
            print  '-------------------------------------'
            print 'Doing backtest for "'+str(exchange)+'" exchange'
            print days_backwards,'days backwards'
            print days_forward,'days forward'
            print 'Symbols:',str(symbols)
            print
            print 'Computations will be made until',all_data_price[-1,0].strftime('%Y-%m-%d'),'is reached'
            print  '-------------------------------------'
            print
        
            
    
    mean_return = np.mean(np.array(backtester_log[1:,1], dtype=float))
    mean_sharpe = np.mean(np.array(backtester_log[1:,2], dtype=float))
    this_backtest = [cumulative_returns, mean_return, mean_sharpe, backtester_log[1,3], dt_end, dt_end_forward]
    backtester_log = np.insert(backtester_log, len(backtester_log),this_backtest, axis=0)
    

    one = 'Backtest from '+str(backtester_log[1,3])+' to '+str(dt_end_forward)+'.'
    two = '-------------------------------------'
    three = 'Cumulative return: '+str(cumulative_returns)
    four = 'Mean return: '+str(mean_return)
    five = 'Mean sharpe: '+str(mean_sharpe)
    six = '-------------------------------------'
    seven = 'Exchange: '+str(exchange)
    eight = 'Symbols: '+str(symbols)
    nine = 'Days backwards: '+str(days_backwards)
    ten = 'Days forward: '+str(days_forward)
    
    filename = dt.datetime.now().strftime('%Y-%m-%d')+'.B'+str(days_backwards)+'.F'+str(days_forward)+'.'+dt.datetime.now().strftime('%H%M%S%f')
    np.savetxt(filename+'.csv', np.array(backtester_log), delimiter=',', fmt="%s")
    save = one+'\r\n '+two+'\r\n '+three+'\r\n '+four+'\r\n '+five+'\r\n '+six+'\r\n '+seven+'\r\n '+eight+'\r\n '+nine+'\r\n '+ten+'\r\n '
    text_file = open(filename+'.txt', "w")
    text_file.write(save)
    text_file.close()
    
    print
    print one
    print two
    print three
    print four
    print five
    print six
    print seven
    print eight
    print nine
    print ten
    

# Call function examples

#symbols = ['EURUSD', 'EURGBP', 'EURCHF', 'EURCAD', 'EURJPY']
#exchange = 'fx'
#allow_short = 1
#days_backwards = 60
#days_forward = 2
#filter_symbols = 0

#symbols = ['ABE', 'FCC', 'IBE', 'SAN', 'REP', 'TEF']
#exchange = 'mc'
#allow_short = 1
#days_backwards = 60
#days_forward = 5
#filter_symbols = 0

symbols = ['ABE', 'ACS', 'AMS', 'ANA', 'BBVA', 'BKT', 'BME', 'CABK', 'DIA', 'ENG', 'FCC', 'FER', 'GAS', 'GRF', 'IAG', 'IBE', 'IDR', 'ITX', 'JAZ', 'MAP', 'OHL', 'POP', 'REE', 'REP', 'SAB', 'SAN', 'TEF', 'TL5', 'TRE', 'VIS']
exchange = 'mc'
allow_short = 1
days_backwards = 4
days_forward = 1
filter_symbols = 4

backtester(symbols, exchange, allow_short, days_backwards, days_forward, filter_symbols)
