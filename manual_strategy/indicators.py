import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

def author():
	return 'ssrishti3'

def SMA(normed_prices, start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31)):
	#calculate SMA with window size 20
	SMA = normed_prices.rolling(window=20,center=False).mean()
	SMA = SMA.bfill()

	#plot graph
	fig,ax=plt.subplots()
	plt.title("SMA indicator")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Price")
	plt.plot(normed_prices , label="price_JPM")
	plt.plot(SMA, label="SMA")
	plt.plot(normed_prices/SMA , label="price_JPM/SMA")
	plt.legend()
	plt.savefig("SMA.png")

def Bollinger_Bands(normed_prices, start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31)):
	#calculate SMA with window size 20
	SMA = normed_prices.rolling(window=20,center=False).mean()
	SMA = SMA.bfill()

	#calculate STD
	STD_DEV = normed_prices.rolling(window=20, center=False).std()
	STD_DEV = STD_DEV.bfill()

	#upper band and lower band, taking c=2
	upper_band = SMA + 2*STD_DEV
	lower_band = SMA - 2*STD_DEV

	bb_value = (normed_prices - SMA)/(2 * STD_DEV)

	fig,ax=plt.subplots()
	plt.title("Bollinger Bands indicator")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Price")
	plt.plot(upper_band , label="upper band")
	plt.plot(SMA, label="SMA")
	plt.plot(bb_value, label="BB Value")
	plt.plot(lower_band , label="lower_band")
	plt.legend()
	plt.savefig("Bollinger_Bands.png")

def CCI(normed_prices, start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31)):
	#calculate SMA with window size 20
	SMA = normed_prices.rolling(window=20,center=False).mean()
	SMA = SMA.bfill()

	#calculate STD
	STD_DEV = normed_prices.rolling(window=20, center=False).std()
	STD_DEV = STD_DEV.bfill()

	constant = 1.0
	CCI = (normed_prices  - SMA) / (constant * STD_DEV)

	#plot
	fig,ax=plt.subplots()
	plt.title("Commodity Channel Index indicator")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Price")
	plt.plot(CCI , label="Commodity Channel Index")
	#plt.plot(normed_prices, label="prices_JPM")
	plt.legend()
	plt.savefig("CCI.png")

def momentum(normed_prices, start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31)):
	momentum = (normed_prices - normed_prices.shift(20))/normed_prices.shift(20)

	#plot
	fig,ax=plt.subplots()
	plt.title("Momentum indicator")
	plt.xlabel("Date")
	plt.xticks(rotation=13)
	plt.ylabel("Normalized Price")
	plt.plot(momentum , label="Momentum")
	plt.legend()
	plt.savefig("momentum.png")


def calculate_and_plot_indicators():
	register_matplotlib_converters()

	symbol = ['JPM']
	start_date = dt.datetime(2008,1,1)
	end_date = dt.datetime(2009,12,31)

	market_dates = pd.date_range(start_date,end_date)
	prices_JPM = get_data(symbol,market_dates)

	#normalize prices
	normed_prices = prices_JPM/prices_JPM.iloc[0]

	#extract JPM price
	normed_prices = normed_prices["JPM"]

	#Indicator1: SMA
	SMA(normed_prices,start_date,end_date)

	#Indicator2: Bollinger Bands
	Bollinger_Bands(normed_prices,start_date,end_date)

	#Indicator3: Commodity Channel Index
	CCI(normed_prices,start_date,end_date)

	#Indicator4: Momentum
	momentum(normed_prices,start_date,end_date)

if __name__ == '__main__':
	calculate_and_plot_indicators()
