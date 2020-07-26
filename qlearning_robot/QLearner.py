"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import random as rand  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class QLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		   	  			  	 		  		  		    	 		 		   		 		  
        self.s = 0  		   	  			  	 		  		  		    	 		 		   		 		  
        self.a = 0  

        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        #reserve space for keeping track of Q[s, a] for the number of states and actions; initialize Q[] with all zeros		
        self.Q = np.zeros((num_states,num_actions))   
        #keep experience history in list	 
        self.exp_hist = [] 			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the state without updating the Q-table  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  	
        #set state to s	   	  			  	 		  		  		    	 		 		   		 		  
        self.s = s 

        #determine action without updating the Q table
        #choose a random action with probability rar
        if np.random.uniform() < self.rar:
          #making random choice in some cases
          action = rand.randint(0, self.Q.shape[1]-1)
        else:
          max = self.Q[s][0]
          action = 0
          for i in range(self.Q.shape[1]):
            if self.Q[s][i]>max:
              max = self.Q[s][i]
              action = i

        self.a = action			  	 		  

        #update random action rate for next update
        self.rar = self.rar*self.radr

        # action = rand.randint(0, self.num_actions-1)  	

        if self.verbose: print(f"s = {s}, a = {action}")  		   	  			  	 		  		  		    	 		 		   		 		  
        return action  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def query(self,s_prime,r):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the Q table and return an action  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s_prime: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @param r: The ne state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        # action = rand.randint(0, self.num_actions-1) 

        #last state  = self.s
        #last action = self.a
        #experience tuple is <s, a, s_prime, r>

        #determine a_prime
        if np.random.uniform() < self.rar:
          #making random choice in some cases
          a_prime = rand.randint(0, self.Q.shape[1]-1)
        else:
          max = self.Q[s_prime][0]
          a_prime = 0
          for i in range(self.Q.shape[1]):
            if self.Q[s_prime][i]>max:
              max = self.Q[s_prime][i]
              a_prime = i 		

        #improve Q using <s,a,s_prime,r>
        curr_Q_est = (1-self.alpha)*self.Q[self.s,self.a]
        imp_Q_est = self.alpha*(r+self.gamma*self.Q[s_prime, a_prime])

        #update the Q table
        self.Q[self.s,self.a] = curr_Q_est + imp_Q_est

        #add to the list of experience tuples
        self.exp_hist.append((self.s, self.a, s_prime, r))

        #update random action rate for next update
        self.rar = self.rar*self.radr

        #s_prime is the new state
        #a_prime is the new action
        self.s = s_prime
        self.a = a_prime

        action=a_prime

        #special case
        #when dyna is not 0
        #one normal Q-learning iteration already done
        if self.dyna:
          #hallucinate additional experiences and update Q table with them
          for i in range(100):
              #select random previously observed state
              random_idx = rand.randint(0,len(self.exp_hist)-1)
              #determine random state and action
              random_s = self.exp_hist[random_idx][0]
              random_a = self.exp_hist[random_idx][1]
              random_s_prime = self.exp_hist[random_idx][2]
              random_r = self.exp_hist[random_idx][3]

              #determine random_a_prime
              if np.random.uniform() < self.rar:
                #making random choice in some cases
                random_a_prime = rand.randint(0, self.Q.shape[1]-1)
              else:
                max = self.Q[random_s_prime][0]
                random_a_prime = 0
                for i in range(self.Q.shape[1]):
                  if self.Q[random_s_prime][i]>max:
                    max = self.Q[random_s_prime][i]
                    random_a_prime = i

              curr_Q_est = (1-self.alpha)*self.Q[random_s,random_a]
              imp_Q_est = self.alpha*(random_r+self.gamma*self.Q[random_s_prime, random_a_prime])

              #update the Q table
              self.Q[random_s,random_a] = curr_Q_est + imp_Q_est

              #update random action rate for next update
              self.rar = self.rar*self.radr

        if self.verbose: print(f"s = {s_prime}, a = {action}, r={r}")  		   	  			  	 		  		  		    	 		 		   		 		  
        return action  		   	  		

    def author(self):
        return 'ssrishti3' # replace tb34 with your Georgia Tech username.	  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		   	  			  	 		  		  		    	 		 		   		 		  
