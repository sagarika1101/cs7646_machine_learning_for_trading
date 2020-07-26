import pandas as pd  
import numpy as np
import datetime as dt  		   	
import os  		   
from util import get_data, plot_data
import matplotlib.pyplot as plt
import marketsimcode as msc
from pandas.plotting import register_matplotlib_converters

def author():
	return 'ssrishti3'

def testPolicy(symbol = "AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
	register_matplotlib_converters()
	market_dates = pd.date_range(sd,ed)

	prices_JPM = get_data(symbol,market_dates)
	prices_JPM = prices_JPM['JPM']
	normed_prices = prices_JPM/prices_JPM.iloc[0]
	normed_prices = normed_prices.to_frame()

	trades_df = pd.DataFrame(index=normed_prices.index)

	#initialzing trades_df values
	trades_df['Symbol'] = 'JPM'
	trades_df['Order'] = np.NaN
	trades_df['Shares'] = 1000.0

	current_holdings = 0.0

	for i in range(0,trades_df.shape[0] - 1):
		#Check if price tomorrow is more and holdings are 0 or -1000
		if (normed_prices.iloc[i+1,0] > normed_prices.iloc[i,0]) and (current_holdings==0.0 or current_holdings==(-1000.0)):
			trades_df.iloc[i,1] = 'BUY'
			current_holdings+=1000.0
		#Check if price tomorrow is less and holdings are 0 or +1000
		elif (normed_prices.iloc[i+1,0] < normed_prices.iloc[i,0]) and (current_holdings==0.0 or current_holdings==1000.0):
			trades_df.iloc[i,1] = 'SELL'
			current_holdings-=1000.0
		else:
			continue

	#Remove days in which no trade is being made
	trades_df.dropna(inplace=True)
	#trades_df is the trades dataframe that we can pass to computer_portvals to compute protfolio values

	return trades_df

def call_test_policy():
	symbol = ['JPM']
	start_date =  dt.datetime(2008,1,1)
	end_date = 	 dt.datetime(2009,12,31)
	start_val = 100000

	trades_df = testPolicy(symbol,start_date,end_date,start_val)
	portvals = msc.compute_portvals(trades_df, 100000, 0.0, 0.0, start_date, end_date)

	#Benchmark: Starting cash: $100,000, investing in 1000 shares of JPM and holding that position.
	bench_trades = trades_df
	#BUY 1000 JPM on day1
	bench_trades.iloc[0,1] = 'BUY'
	for i in range(1,bench_trades.shape[0]):
		bench_trades.iloc[i,1] = np.NaN
	bench_trades.dropna(inplace=True)
	bench_portvals = msc.compute_portvals(bench_trades, 100000, 0.0, 0.0, start_date, end_date)

	#plot portvals and bench_portvals
	#normalize
	portvals = portvals/portvals.iloc[0]
	bench_portvals = bench_portvals/bench_portvals.iloc[0]
	#plot
	fig,ax=plt.subplots()
	plt.title("Theoretically Optimal Strategy vs. Benchmark")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Portfolio Value")
	plt.plot(portvals , 'r', label="Theoretically Optimal Strategy")
	plt.plot(bench_portvals, 'g', label="Benchmark")
	plt.legend()
	plt.savefig("PortvalVsBenchmark.png")

	#calculate statistics
	#cumulative return
	cr_port = portvals.iloc[-1]/portvals.iloc[0] - 1
	cr_bench = bench_portvals.iloc[-1]/bench_portvals.iloc[0] - 1
	print("Cumulative return of Theoretically Optimal Strategy: " + str(cr_port))
	print("Cumulative return of Benchmark: " + str(cr_bench))

	#standard deviation
	daily_ret_port = (portvals/portvals.shift(1)) -1
	daily_ret_bench = (bench_portvals/bench_portvals.shift(1)) -1
	std_port = daily_ret_port.std()
	std_bench = daily_ret_bench.std()
	print("Standard Deviation of Daily Returns Theoretically Optimal Strategy: " + str(std_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(std_bench))

	#Mean
	mean_port = daily_ret_port.mean()
	mean_bench = daily_ret_bench.mean()
	print("Mean of Daily Returns of Theoretically Optimal Strategy: " + str(mean_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(mean_bench))

if __name__ == '__main__':
	call_test_policy()