"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: ssrishti3 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903511279 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import util as ut  		   	  			  	 		  		  		    	 		 		   		 		  
import random  		

import RTLearner as rt
import BagLearner as bg
from indicators import *
import ManualStrategy as ms   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # constructor  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.impact = impact  
        #determining learner, all other parameters left as default: leaf_size 5, bags: 20
        self.learner = bg.BagLearner(learner = rt.RTLearner)		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # add your code to do learning here  	
        # example usage of the old backward compatible util function 
        #extracting prices       
        syms=[symbol]
        dates = pd.date_range(sd, ed) 
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose:
          print(prices)

        #adding indicators as extra features
        #normalize prices
        normed_prices = prices/prices.iloc[0]
        #SMA
        SM = SMA(normed_prices,sd,ed)
        SM.columns = ['SMA']
        #Commodity Channel Index
        CC = CCI(normed_prices,sd,ed)
        CC.columns = ['CCI']
        #Momentum
        mom = momentum(normed_prices,sd,ed)
        mom.columns = ['momentum']
        X_train = pd.concat((normed_prices,SM,CC,mom),axis=1)
        X = np.array(X_train)

        #making Y train
        #taking lookforward period of 10 days
        Y = (prices.shift(-1 * 10) / prices - 1)
        Y = Y.fillna(0.0)
        # Y = np.array(Y)
        for i in range(Y.shape[0] - 10):
          if Y.iloc[i][0] > self.impact:
            Y.iloc[i][0] = 1.0
          elif Y.iloc[i][0] < -self.impact:
            Y.iloc[i][0] = -1.0
          else:
            Y.iloc[i][0] = 0.0
        Y = np.array(Y)

        #train learner
        self.learner.addEvidence(X,Y)   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # # example usage of the old backward compatible util function  		   	  			  	 		  		  		    	 		 		   		 		  
        # syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
        # dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(prices)  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # # example use with new colname  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume = volume_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # volume_SPY = volume_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(volume)  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			  	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		

        #extracting prices  
        syms=[symbol]
        dates = pd.date_range(sd, ed) 
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols

        #adding indicators as extra features
        #normalize prices
        normed_prices = prices/prices.iloc[0]
        #SMA
        SM = SMA(normed_prices,sd,ed)
        SM.columns = ['SMA']
        #Commodity Channel Index
        CC = CCI(normed_prices,sd,ed)
        CC.columns = ['CCI']
        #Momentum
        mom = momentum(normed_prices,sd,ed)
        mom.columns = ['momentum']
        X_train = pd.concat((normed_prices,SM,CC,mom),axis=1)
        X = np.array(X_train)

        #predictions
        Y = self.learner.query(X)

        #make trades based on Y
        trades_df = normed_prices
        trades_df.values[:,:] = 0.0
        current_holdings = 0.0

        for i in range(0,trades_df.shape[0]):
          if Y[i] == 1.0:
            if current_holdings==0.0:
              trades_df.values[i,:] = 1000.0
              current_holdings+=1000.0
            if current_holdings==(-1000.0):
              trades_df.values[i,:] = 2000.0
              current_holdings+=2000.0
          elif Y[i] == -1.0:
            if current_holdings==0.0:
              trades_df.values[i,:] = -1000.0
              current_holdings-=1000.0
            if current_holdings==1000.0:
              trades_df.values[i,:] = (-2000.0)
              current_holdings-=2000.0
          else:
            trades_df.values[i,:] = 0.0

        return trades_df  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # here we build a fake set of trades  		   	  			  	 		  		  		    	 		 		   		 		  
        # your code should return the same sort of data  		   	  			  	 		  		  		    	 		 		   		 		  
        # dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades = prices_all[[symbol,]]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[:,:] = 0 # set them all to nothing  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[0,:] = 1000 # add a BUY at the start  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[40,:] = -1000 # add a SELL  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[41,:] = 1000 # add a BUY  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[60,:] = -2000 # go short from long  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[61,:] = 2000 # go long from short  		   	  			  	 		  		  		    	 		 		   		 		  
        # trades.values[-1,:] = -1000 #exit on the last day  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(type(trades)) # it better be a DataFrame!  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(trades)  		   	  			  	 		  		  		    	 		 		   		 		  
        # if self.verbose: print(prices_all)  		   	  			  	 		  		  		    	 		 		   		 		  
        # return trades  		

    def author():
        return 'ssrishti3' # replace tb34 with your Georgia Tech username. 	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		   	  			  	 		  		  		    	 		 		   		 		  
