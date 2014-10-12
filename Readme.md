## Data

> Data is retrieved from Quandl. An **API key is needed** in order to make more than 50 queries a day. **Include it at the beginning of get_data.py**

## Dependencies

- Python:
	+ quandl
	+ numpy
	+ pandas

## def allocation_op(symbols, exchange, allow_short, days = None, filter_symbols = 5, data_allocate = None, dt_start = None, dt_end = None)

> Tests all possible portfolio allocations for **symbols** and determines which one had the **best Sharpe ratio** for the period [today - *days*] to today _or_ from *dt_start* to *dt_end*.
> **File: allocation_sharpe_optimizer.py**

- symbols (list): 
	+ ['EURUSD', 'EURCAD']
	+ ['ABE', 'FCC', 'IBE', 'SAN', 'REP', 'TEF']
	
- exchange (string): Data is extracted from Quandl (get_data.py). It inserts the corresponding sufix and prefix to the 'nude' symbols.
	+ 'fx': Forex. Reformats symbols QUANDL/symbols[i].1 to get the prices column of Forex pairs.
	+ 'mc': Madrid -> YAHOO/MC_symbols[i].4 -> Closing prices for Madrid.
	+ 'custom': All symbols will include Quandl prefix and the column where daily closing prices are for that symbol
		* ['QUANDL/EURUSD.1', 'YAHOO/MC_ABE.4', 'QUANDL/EURCAD.1', 'YAHOO/MC_FCC.4']

- allow_short (integer): Allow for short positions when computing the ideal investment/allocation.
	+ 1: Yes
	+ 0: No

- days (integer): Number of days from any given point in the 'present' the computation/data for the ideal investment/allocation will go back.

- filter_symbols (integer; default value is 5; 0 to turn off): In order to compute the best allocations, a matrix for all the possible ones (all_permutes.py) is created. The algorithm that creates it has an enormous order of growth; this requires computational power, time, memory. Plus, every iteration of the test to find the best allocation for every moment in time (allocation_op) will take longer (which is a pain, particularly when backtesting), as it'll have to test for more and more possibilities. It is advisable to keep this under 6, and definitively under 10. So:
	+ There will be a pre-selection of symbols if symbols > filter_symbols for each iteration of allocation_op (for each point in time an allocation/investment is computed) choosing only those with the best sharpe ratio, and testing only those for possible different allocations within them.
	
- data_allocate (numpy array): If not provided, allocation_op will take it from Quandl. If provided, it should have the dates (datetime) in the first field for each row, and the values of each closing price for each symbol in the same order as *symbols*.

- dt_start and dt_end: They might be used **instead** of *days* to compute the best allocation for some range of dates ending in the past (not for the day the computation is made, but before).

## backtester(symbols, exchange, allow_short, days_backwards, days_forward, filter_symbols = 5)

> Backtest of allocation_op. It will use all historical data available for the symbols.
> It will save the the cumulative returns, the returns per period, and the sharpe ratio of the portfolio, in a csv file.
> **File: backtester.py**

- days_backwards (integer): Number of days to be passed to allocation_op

- days_forward (integer): Number of days the investment made in the symbols and allocations computed for days_backwards will be held. At the end of this period, a new computation would be done (for 'present day - days_backards' to 'present day') taking this moment as the new 'present day', which would start a new investment to be hold, again for 'days_forward' days.

## simulate(na_price_nodate, dt_start, dt_end, symbols, portf_allocation)

> Returns sharpe ratio and returns for some portfolio.
> **File: simulate_portfolio_allocation.py**

- na_price_nodate (numpy array): Same as *data_allocate* but without the date on the first field.

- symbols (list): If they have a minus sign as the first character, sharpe and returns will be computed for a **short position**.

- portf_allocation (list): Allocation for each symbol (same order).
	+ [0.3, 0.0, 0.7]
	+ [0.4, 0.6]

## To check

> **Errors* might - they probably do - exist. All the computing modules/functions should be checked.

- Does all_permutes.py actually create data for all possible values?
- Does *simulate* (simulate_portfolio_allocation.py) work well?
- Does *allocation_op* (allocation_sharpe_optimizer.py) work well?
- Does *backtester* (backtester.py) work well?

## To-do (future):

- "Events" detection -> Probably better to do in NinjaTrader or MT4?

- Drawdown -> Compute max drawdown for the analized period and put stop loss for investment

## License
GNU Lesser General Public License, version 2.1