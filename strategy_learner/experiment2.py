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

def calculate_and_print_stats(portvals,impact=None):
	#calculate statistics
	#cumulative return
	cr = portvals.iloc[-1]/portvals.iloc[0] - 1
	if impact:
		print("Cumulative return for impact value " + impact + ":" + str(cr))
	else:
		print('Cumulative return: ' + str(cr))

	#Sharpe Ratio
	daily_ret_port = (portvals/portvals.shift(1)) -1
	sr = np.sqrt(252.0) * (np.mean((daily_ret_port))/np.std(daily_ret_port))
	if impact:
		print("Sharpe ratio for impact value " + impact + ":" + str(sr))
	else:
		print('Sharpe ratio: ' + str(sr))

if __name__=="__main__": 
	register_matplotlib_converters()
	np.random.seed(903511279)
	symbol = ['JPM']

	#In sample
	sd =  dt.datetime(2008,1,1)
	ed = dt.datetime(2009,12,31)

	#Strategy Learner, impact=0.05
	learner1 = sl.StrategyLearner(verbose = False, impact=0.05)
	learner1.addEvidence('JPM',sd,ed)
	trades_sl1 = learner1.testPolicy('JPM',sd,ed)
	trades1 = pd.DataFrame(index=trades_sl1.index)
	trades1['Symbol'] ='JPM'
	trades1['Order'] = np.NaN
	trades1['Shares'] = 1000.0
	for index,row in trades_sl1.iterrows():
		if float(row['JPM']) == 1000.0:
			trades1.loc[index,'Order'] = 'BUY'
		if float(row['JPM']) == -1000.0:
			trades1.loc[index,'Order'] = 'SELL'
		if float(row['JPM']) == 2000.0:
			trades1.loc[index,'Order'] = 'BUY'
			trades1.loc[index,'Shares'] = 2000.0
		if float(row['JPM']) == -2000.0:
			trades1.loc[index,'Order'] = 'SELL'
			trades1.loc[index,'Shares'] = 2000.0
	trades1.dropna(inplace=True)
	sl_portvals1 = msc.compute_portvals(trades1, 100000.0, 0.0, 0.05, sd, ed)

	#Strategy Learner, impact=0.005
	learner2 = sl.StrategyLearner(verbose = False, impact=0.005)
	learner2.addEvidence('JPM',sd,ed)
	trades_sl2 = learner2.testPolicy('JPM',sd,ed)
	trades2 = pd.DataFrame(index=trades_sl2.index)
	trades2['Symbol'] ='JPM'
	trades2['Order'] = np.NaN
	trades2['Shares'] = 1000.0
	for index,row in trades_sl2.iterrows():
		if float(row['JPM']) == 1000.0:
			trades2.loc[index,'Order'] = 'BUY'
		if float(row['JPM']) == -1000.0:
			trades2.loc[index,'Order'] = 'SELL'
		if float(row['JPM']) == 2000.0:
			trades2.loc[index,'Order'] = 'BUY'
			trades2.loc[index,'Shares'] = 2000.0
		if float(row['JPM']) == -2000.0:
			trades2.loc[index,'Order'] = 'SELL'
			trades2.loc[index,'Shares'] = 2000.0
	trades2.dropna(inplace=True)
	sl_portvals2 = msc.compute_portvals(trades2, 100000.0, 0.0, 0.005, sd, ed)

	#Strategy Learner, impact=0.0005
	learner3 = sl.StrategyLearner(verbose = False, impact=0.0005)
	learner3.addEvidence('JPM',sd,ed)
	trades_sl3 = learner3.testPolicy('JPM',sd,ed)
	trades3 = pd.DataFrame(index=trades_sl3.index)
	trades3['Symbol'] ='JPM'
	trades3['Order'] = np.NaN
	trades3['Shares'] = 1000.0
	for index,row in trades_sl3.iterrows():
		if float(row['JPM']) == 1000.0:
			trades3.loc[index,'Order'] = 'BUY'
		if float(row['JPM']) == -1000.0:
			trades3.loc[index,'Order'] = 'SELL'
		if float(row['JPM']) == 2000.0:
			trades3.loc[index,'Order'] = 'BUY'
			trades3.loc[index,'Shares'] = 2000.0
		if float(row['JPM']) == -2000.0:
			trades3.loc[index,'Order'] = 'SELL'
			trades3.loc[index,'Shares'] = 2000.0
	trades3.dropna(inplace=True)
	sl_portvals3 = msc.compute_portvals(trades3, 100000.0, 0.0, 0.0005, sd, ed)

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

	#plot
	#normalize
	sl_portvals1 = sl_portvals1/sl_portvals1.iloc[0]
	sl_portvals2 = sl_portvals2/sl_portvals2.iloc[0]
	sl_portvals3 = sl_portvals3/sl_portvals3.iloc[0]
	bench_portvals = bench_portvals/bench_portvals.iloc[0]

	fig,ax=plt.subplots()
	plt.title("Strategy Learner with different impact values")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Portfolio Value")
	plt.plot(sl_portvals1 , 'r', label="Strategy Learner impact=0.05")
	plt.plot(sl_portvals2, 'g', label="Strategy Learner impact=0.005")
	plt.plot(sl_portvals3, 'b', label="Strategy Learner impact=0.0005")
	plt.plot(bench_portvals,'y',label='Benchmark')
	plt.legend()
	plt.savefig("exp2_new1.png")

	#statistics
	calculate_and_print_stats(sl_portvals1,'0.05')
	calculate_and_print_stats(sl_portvals2,'0.005')
	calculate_and_print_stats(sl_portvals3,'0.0005')
	calculate_and_print_stats(bench_portvals)