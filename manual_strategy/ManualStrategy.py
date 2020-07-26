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

	#calculate SMA and momentum
	SMA = normed_prices.rolling(window=20,center=False).mean()
	SMA = SMA.bfill()
	momentum = (normed_prices - normed_prices.shift(20))/normed_prices.shift(20)
	momentum = momentum.bfill()

	current_holdings = 0.0
	for i in range(trades_df.shape[0]):
		#Check if SMA<0.95 or momentum<-0.5
		if (SMA.iloc[i,0] < 0.98 or momentum.iloc[i,0] < -0.6) and (current_holdings==0.0 or current_holdings==(-1000.0)):
			trades_df.iloc[i,1] = 'BUY'
			current_holdings+=1000.0
		#Check if SMA>1.05 or momentum>0.5
		elif (SMA.iloc[i,0] > 1.08 or momentum.iloc[i,0] > 0.6) and (current_holdings==0.0 or current_holdings==1000.0):
			trades_df.iloc[i,1] = 'SELL'
			current_holdings-=1000.0
		else:
			continue    

	#Remove days in which no trade is being made
	trades_df.dropna(inplace=True)
	#trades_df is the trades dataframe that we can pass to computer_portvals to compute protfolio values

	return trades_df

def call_test_policy():
	register_matplotlib_converters()

	symbol = ['JPM']
	in_start_date =  dt.datetime(2008,1,1)
	in_end_date = dt.datetime(2009,12,31)
	out_start_date = dt.datetime(2010,1,1)
	out_end_date = dt.datetime(2011,12,31)

	trades_df = testPolicy(symbol,in_start_date,in_end_date,100000.0)
	portvals = msc.compute_portvals(trades_df, 100000, 9.95, 0.005, in_start_date, in_end_date)

	#Benchmark: Starting cash: $100,000, investing in 1000 shares of JPM and holding that position.
	market_dates = pd.date_range(in_start_date,in_end_date)

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

	bench_portvals = msc.compute_portvals(bench_trades, 100000, 9.95, 0.005, in_start_date, in_end_date)

	#plot portvals and bench_portvals
	#normalize
	portvals = portvals/portvals.iloc[0]
	bench_portvals = bench_portvals/bench_portvals.iloc[0]

	fig,ax=plt.subplots()
	plt.title("Manual Rule-based Strategy vs. Benchmark")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Portfolio Value")
	plt.plot(portvals , 'r', label="Manual Rule-based Strategy")
	plt.plot(bench_portvals, 'g', label="Benchmark")
	plt.legend()
	for index, item in trades_df.iterrows():
		if item['Order'] == 'SELL':
			ax.axvline(index, color="blue")
		elif item['Order'] == 'BUY':
			ax.axvline(index, color="black")
	plt.savefig("In_sample_manual.png")

	#calculate statistics
	#cumulative return
	print("In-sample Statistics")
	cr_port = portvals.iloc[-1]/portvals.iloc[0] - 1
	cr_bench = bench_portvals.iloc[-1]/bench_portvals.iloc[0] - 1
	print("Cumulative return of Manual Rule-Based Strategy: " + str(cr_port))
	print("Cumulative return of Benchmark: " + str(cr_bench))

	#standard deviation
	daily_ret_port = (portvals/portvals.shift(1)) -1
	daily_ret_bench = (bench_portvals/bench_portvals.shift(1)) -1
	std_port = daily_ret_port.std()
	std_bench = daily_ret_bench.std()
	print("Standard Deviation of Daily Returns Manual Rule-Based Strategy: " + str(std_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(std_bench))

	#Mean
	mean_port = daily_ret_port.mean()
	mean_bench = daily_ret_bench.mean()
	print("Mean of Daily Returns of Manual Rule-Based Strategy: " + str(mean_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(mean_bench))

	#out-sample portfolio
	out_trades_df = testPolicy(symbol,out_start_date,out_end_date,100000.0)
	out_portvals = msc.compute_portvals(out_trades_df, 100000, 9.95, 0.005, out_start_date, out_end_date)

	#Out-sample Benchmark: Starting cash: $100,000, investing in 1000 shares of JPM and holding that position.
	out_market_dates = pd.date_range(out_start_date,out_end_date)

	out_prices_JPM = get_data(symbol,out_market_dates)
	out_prices_JPM = out_prices_JPM['JPM']
	out_normed_prices = out_prices_JPM/out_prices_JPM.iloc[0]
	out_normed_prices = out_normed_prices.to_frame()
	out_bench_trades = pd.DataFrame(index=out_normed_prices.index)
	#initialzing bench_trades values
	out_bench_trades['Symbol'] ='JPM'
	out_bench_trades['Order'] = np.NaN
	out_bench_trades['Shares'] = 1000.0
	#BUY 1000 JPM on day1
	out_bench_trades.iloc[0,1] = 'BUY'
	for i in range(1,out_bench_trades.shape[0]):
		out_bench_trades.iloc[i,1] = np.NaN
	out_bench_trades.dropna(inplace=True)

	out_bench_portvals = msc.compute_portvals(out_bench_trades, 100000, 9.95, 0.005, out_start_date, out_end_date)

	#plot out_portvals and bench_portvals
	#normalize
	out_portvals = out_portvals/out_portvals.iloc[0]
	out_bench_portvals = out_bench_portvals/out_bench_portvals.iloc[0]

	fig,ax=plt.subplots()
	plt.title("Manual Rule-based Strategy vs. Benchmark")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Portfolio Value")
	plt.plot(out_portvals , 'r', label="Manual Rule-based Strategy")
	plt.plot(out_bench_portvals, 'g', label="Benchmark")
	plt.legend()
	plt.savefig("Out_sample_manual.png")

	#calculate statistics
	print("Out-sample Statistics")
	#cumulative return
	out_cr_port = out_portvals.iloc[-1]/out_portvals.iloc[0] - 1
	out_cr_bench = out_bench_portvals.iloc[-1]/out_bench_portvals.iloc[0] - 1
	print("Cumulative return of Manual Rule-Based Strategy: " + str(out_cr_port))
	print("Cumulative return of Benchmark: " + str(out_cr_bench))

	#standard deviation
	out_daily_ret_port = (out_portvals/out_portvals.shift(1)) -1
	out_daily_ret_bench = (out_bench_portvals/out_bench_portvals.shift(1)) -1
	out_std_port = out_daily_ret_port.std()
	out_std_bench = out_daily_ret_bench.std()
	print("Standard Deviation of Daily Returns Manual Rule-Based Strategy: " + str(out_std_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(out_std_bench))

	#Mean
	out_mean_port = out_daily_ret_port.mean()
	out_mean_bench = out_daily_ret_bench.mean()
	print("Mean of Daily Returns of Manual Rule-Based Strategy: " + str(out_mean_port))
	print("Standard Deviation of Daily Returns of Benchmark: " + str(out_mean_bench))

if __name__ == '__main__':
	call_test_policy()
	