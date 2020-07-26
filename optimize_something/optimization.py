"""MC1-P2: Optimize a portfolio.                                                                
                                                                
Copyright 2018, Georgia Institute of Technology (Georgia Tech)                                                                
Atlanta, Georgia 30332                                                                
All Rights Reserved                                                               
                                                                
Template code for CS 4646/7646                                                                
                                                                
Georgia Tech asserts copyright ownership of this template and all derivative                                                                
works, including solutions to the projects assigned in this course. Students                                                                
and other users of this template code are advised not to share it with others                                                               
or to make it available on publicly viewable websites including repositories                                                                
such as github and gitlab.  This copyright statement should not be removed                                                                
or edited.                                                                
                                                                
We do grant permission to share solutions privately with non-students such                                                                
as potential employers. However, sharing with other current or future                                                               
students of CS 7646 is prohibited and subject to being investigated as a                                                                
GT honor code violation.                                                                
                                                                
-----do not edit anything above this line---                                                                
                                                                
Student Name: Sagarika Srishti (replace with your name)                                                               
GT User ID: ssrishti3 (replace with your User ID)                                                                
GT ID: 903511279 (replace with your GT ID)                                                                
"""                                                               
                                                                
                                                                
import pandas as pd                                                               
import matplotlib.pyplot as plt                                                               
import numpy as np                                                                
import datetime as dt                                                               
from util import get_data, plot_data    
import scipy.optimize as spo
from pandas.plotting import register_matplotlib_converters

def calc_inv_sr(allocs,cum_ret,rfr,td):
  port_daily = cum_ret * allocs   #assigning allocations
  #taking starting value to be 1.0 so not multiplying by amount
  port_daily = port_daily.sum(axis=1)  #1-D array of daily portfolio values

  daily_ret = (port_daily/port_daily.shift(1)) -1 #calculating daily returns
  sr = np.sqrt(td) * (np.mean((daily_ret - rfr))/np.std(daily_ret)) #check again
  inv_sr = 1.0/sr  #will minimize 1/sr to maximize sr

  return inv_sr

                                                                
# This is the function that will be tested by the autograder                                                                
# The student must update this code to properly implement the functionality                                                               
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):                                                                
                                                                
    # Read in adjusted closing prices for given symbols, date range                                                               
    dates = pd.date_range(sd, ed)                                                               
    prices_all = get_data(syms, dates)  # automatically adds SPY                                                                
    prices = prices_all[syms]  # only portfolio symbols                                                               
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later  

    #initialising constants
    rfr = 0.0   #risk free return
    td = 252.0  #trading days in a year
    #inital allocation
    allocs = np.full((len(syms)), (1/len(syms)), dtype=float)
    cum_ret = prices / prices.values[0]   #calculating cumulative return 

    #bounds and constraints
    bounds = [(0.0,1.0) for i in allocs] #size of allocs = number of stocks
    constraints = ({ 'type':'eq', 'fun':lambda inputs: 1.0 - np.sum(inputs)}) #check
                      
    # find the allocations for the optimal portfolio                                                                
    # note that the values here ARE NOT meant to be correct for a test case                                                               
    #allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations 

    result = spo.minimize(calc_inv_sr, allocs, args = (cum_ret,rfr,td,), \
      method='SLSQP', bounds=bounds, constraints=constraints)  

    optimal_allocs = result.x
    sr = np.power(result.fun, -1)


    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    #cum_ret = prices / prices.values[0]  #calculating cumulative return
    cum_ret = cum_ret * optimal_allocs  
    port_daily = cum_ret.sum(axis=1)

    daily_ret = (port_daily/port_daily.shift(1)) -1 
    adr = np.mean(daily_ret)
    sddr = np.std(daily_ret)
    cr= (port_daily[-1]/port_daily[0]) - 1  
    allocs=optimal_allocs
    sr=np.sqrt(td) * np.mean((daily_ret - rfr)) / np.std(daily_ret)    

                                                          
    # Get daily portfolio value                                                               
    #port_val = prices_SPY # add code here to compute daily portfolio values                                                               
                                                                
    # Compare daily portfolio value with SPY using a normalized plot                                                                
    if gen_plot:                                                                
        # add code to plot here    
        prices_SPY = prices_SPY / prices_SPY[0]   
        port_daily = port_daily/ port_daily[0]                                                        
        df_temp = pd.concat([port_daily, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)   
        #plot_data(df_temp, title="Daily portfolio value vs SPY")
        plt.plot(df_temp)
        plt.title("Daily portfolio value vs SPY")
        plt.savefig("fig1.png")                                                            
        pass                                                                
                                                                
    return allocs, cr, adr, sddr, sr                                                                
                                                                
def test_code():                                                                
    # This function WILL NOT be called by the auto grader                                                               
    # Do not assume that any variables defined here are available to your function/code                                                               
    # It is only here to help you set up and test your code                                                               
                                                                
    # Define input parameters                                                               
    # Note that ALL of these values will be set to different values by                                                                
    # the autograder!             

    register_matplotlib_converters()

                                                                
    start_date = dt.datetime(2008,6,1)                                                                
    end_date = dt.datetime(2009,6,1)                                                                
    symbols = ['IBM', 'X', 'GLD', 'JPM']                                                               
                                                                
    # Assess the portfolio                                                                
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)                                                               
                                                                
    # Print statistics                                                                
    print(f"Start Date: {start_date}")                                                                
    print(f"End Date: {end_date}")                                                                
    print(f"Symbols: {symbols}")                                                                
    print(f"Allocations:{allocations}")                                                               
    print(f"Sharpe Ratio: {sr}")                                                                
    print(f"Volatility (stdev of daily returns): {sddr}")                                                               
    print(f"Average Daily Return: {adr}")                                                               
    print(f"Cumulative Return: {cr}")                                                               
                                                                
if __name__ == "__main__":                                                                
    # This code WILL NOT be called by the auto grader                                                               
    # Do not assume that it will be called                                                                
    test_code()                                                               
