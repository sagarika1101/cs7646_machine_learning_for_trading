import datetime as dt  		 
import pandas as pd  
import util as ut  	
import random
from pandas.plotting import register_matplotlib_converters
import RTLearner as rt
import BagLearner as bg
from indicators import *
import ManualStrategy as ms
import marketsimcode as msc
import StrategyLearner as sl

def author():
	return 'ssrishti3'

def calculate_and_print_stats(portvals,strategy_name):
	#calculate statistics
	#cumulative return
	cr = portvals.iloc[-1]/portvals.iloc[0] - 1
	print("Cumulative return of " + strategy_name + ":" + str(cr))

	#standard deviation
	daily_ret_port = (portvals/portvals.shift(1)) -1
	std_port = daily_ret_port.std()
	print("Standard Deviation of Daily Returns of " + strategy_name + ":" + str(std_port))

	#Mean
	mean_port = daily_ret_port.mean()
	print("Mean of Daily Returns of " + strategy_name + ":" + str(mean_port))

if __name__=="__main__": 
	register_matplotlib_converters()
	np.random.seed(903511279)
	symbol = ['JPM']

	#In sample
	sd =  dt.datetime(2008,1,1)
	ed = dt.datetime(2009,12,31)

	#Manual Strategy
	trades_df = ms.testPolicy(symbol,sd,ed,100000.0)
	portvals = msc.compute_portvals(trades_df, 100000, 0.0, 0.005, sd, ed)

	#Benchmark: Starting cash: $100,000, investing in 1000 shares of JPM and holding that position.
	market_dates = pd.date_range(sd,ed)
	prices_JPM = get_data(symbol,market_dates)
	prices_JPM = prices_JPM['JPM']
	normed_prices = prices_JPM/prices_JPM.iloc[0]
	normed_prices = normed_prices.to_frame()
	bench_trades = pd.DataFrame(index=normed_prices.index)
	#initialzing bench_trades values
	bench_trades['Symbol'] ='JPM'
	bench_trades['Order'] = np.NaN
	bench_trades['Shares'] = 1000.0
	#BUY 1000 JPM on day1
	bench_trades.iloc[0,1] = 'BUY'
	for i in range(1,bench_trades.shape[0]):
		bench_trades.iloc[i,1] = np.NaN
	bench_trades.dropna(inplace=True)
	bench_portvals = msc.compute_portvals(bench_trades, 100000, 0.0, 0.0, sd, ed)

	#Strategy Learner
	learner = sl.StrategyLearner(verbose = False, impact=0.005)
	learner.addEvidence('JPM',sd,ed)
	trades_sl = learner.testPolicy('JPM',sd,ed)
	trades = pd.DataFrame(index=trades_sl.index)
	trades['Symbol'] ='JPM'
	trades['Order'] = np.NaN
	trades['Shares'] = 1000.0
	for index,row in trades_sl.iterrows():
		if float(row['JPM']) == 1000.0:
			trades.loc[index,'Order'] = 'BUY'
		if float(row['JPM']) == -1000.0:
			trades.loc[index,'Order'] = 'SELL'
		if float(row['JPM']) == 2000.0:
			trades.loc[index,'Order'] = 'BUY'
			trades.loc[index,'Shares'] = 2000.0
		if float(row['JPM']) == -2000.0:
			trades.loc[index,'Order'] = 'SELL'
			trades.loc[index,'Shares'] = 2000.0
	trades.dropna(inplace=True)
	sl_portvals = msc.compute_portvals(trades, 100000, 0.0, 0.005, sd, ed)

	#plot
	#normalize
	portvals = portvals/portvals.iloc[0]
	bench_portvals = bench_portvals/bench_portvals.iloc[0]
	sl_portvals = sl_portvals/sl_portvals.iloc[0]

	fig,ax=plt.subplots()
	plt.title("Manual Strategy vs. Strategy Learner")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Portfolio Value")
	plt.plot(portvals , 'r', label="Manual Rule-based Strategy")
	plt.plot(bench_portvals, 'g', label="Benchmark")
	plt.plot(sl_portvals, 'b', label="Strategy Learner")
	plt.legend()
	plt.savefig("exp1.png")

	#statistics
	calculate_and_print_stats(portvals,"Manual Rule-based Strategy")
	calculate_and_print_stats(bench_portvals,'Benchmark')
	calculate_and_print_stats(sl_portvals,'Strategy Learner')