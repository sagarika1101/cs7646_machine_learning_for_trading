"""Assess a betting strategy.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  
import matplotlib.pyplot as plt

  		   	  			  	 		  		  		    	 		 		   		 		  
def author():  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'ssrishti3' # replace tb34 with your Georgia Tech username.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def gtid():  		   	  			  	 		  		  		    	 		 		   		 		  
	return 903511279 # replace with your GT ID number  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			  	 		  		  		    	 		 		   		 		  
	result = False  		   	  			  	 		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			  	 		  		  		    	 		 		   		 		  
		result = True  		   	  			  	 		  		  		    	 		 		   		 		  
	return result  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
	win_prob = 18.0/38 # set appropriately to the probability of a win  		   	  			  	 		  		  		    	 		 		   		 		  
	np.random.seed(gtid()) # do this only once  		   	  			  	 		  		  		    	 		 		   		 		  
	print(get_spin_result(win_prob)) # test the roulette spin  	
	
	#run experiment 1
	exp1(win_prob)

	#run experiment 2
	exp2(win_prob)	   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
	# add your code here to implement the experiments  

def roulette_spin(episodes,win_prob):
	winnings=np.zeros((episodes,1001),dtype=int)
	for i in range(episodes):
		bet_amount=1
		for j in range(1,1001):
			if get_spin_result(win_prob)==True:
				winnings[i][j]=winnings[i][j-1] + bet_amount
				bet_amount=1
				if winnings[i][j]>=80:
					winnings[i][j:]=80
					break
			else:
				winnings[i][j]=winnings[i][j-1] - bet_amount
				bet_amount*=2
	return winnings

def exp1(win_prob):
	#part (a)
	winnings_a=roulette_spin(10,win_prob)
	#plot
	fig,ax=plt.subplots()
	plt.title("Winnings vs. No of Spins (Exp. 1(a))")
	plt.xlabel("Number of Spins")
	plt.xlim(0,300)
	plt.ylabel("Winnings")
	plt.ylim(-256,100)
	plt.plot(winnings_a.T)
	plt.savefig("exp1a.png")

	#part (b)
	winnings_b=roulette_spin(1000,win_prob)
	#plots
	fig,ax=plt.subplots()
	plt.title("Mean Winnings vs. No of Spins (Exp. 1(b))")
	plt.xlabel("Number of Spins")
	plt.xlim(0,300)
	plt.ylabel("Mean Winnings")
	plt.ylim(-256,100)
	plt.plot(np.mean(winnings_b,axis=0),label="mean")
	plt.plot(np.mean(winnings_b,axis=0)-np.std(winnings_b,axis=0),label="mean-STD")
	plt.plot(np.mean(winnings_b,axis=0)+np.std(winnings_b,axis=0),label="mean+STD")
	plt.legend()
	plt.savefig("exp1b1.png")

	fig,ax=plt.subplots()
	plt.title("Median Winnings vs. No of Spins (Exp. 1(b))")
	plt.xlabel("Number of Spins")
	plt.xlim(0,300)
	plt.ylabel("Median Winnings")
	plt.ylim(-256,100)
	plt.plot(np.median(winnings_b,axis=0),label="median")
	plt.plot(np.median(winnings_b,axis=0)-np.std(winnings_b,axis=0),label="median-STD")
	plt.plot(np.median(winnings_b,axis=0)+np.std(winnings_b,axis=0),label="median+STD")
	plt.legend()
	plt.savefig("exp1b2.png")


def exp2(win_prob):
	winnings=np.zeros((1000,1001),dtype=int)
	bet_amount=1
	for j in range(1000):
		for i in range(1,1001):
		    if get_spin_result(win_prob)==True:
		        winnings[j][i]=winnings[j][i-1] + bet_amount
		        bet_amount=1
		        if winnings[j][i]>=80:
		            winnings[j][i:]=80
		            break
		    else:
		        winnings[j][i]=winnings[j][i-1] - bet_amount
		        if winnings[j][i]<=-256:
		        	winnings[j][i:]=-256
		        	break
		        bet_amount*=2
		        if bet_amount> (winnings[j][i]+256):
		            bet_amount=winnings[j][i]+256

    #plots
	fig,ax=plt.subplots()
	plt.title("Mean Winnings vs. No of Spins (Exp. 2)")
	plt.xlabel("Number of Spins")
	plt.xlim(0,300)
	plt.ylabel("Mean Winnings")
	plt.ylim(-256,100)
	plt.plot(np.mean(winnings,axis=0),label="mean")
	plt.plot(np.mean(winnings,axis=0)-np.std(winnings,axis=0),label="mean-STD")
	plt.plot(np.mean(winnings,axis=0)+np.std(winnings,axis=0),label="mean+STD")
	plt.legend()
	plt.savefig("exp2a.png")

	fig,ax=plt.subplots()
	plt.title("Median Winnings vs. No of Spins (Exp. 2)")
	plt.xlabel("Number of Spins")
	plt.xlim(0,300)
	plt.ylabel("Median Winnings")
	plt.ylim(-256,100)
	plt.plot(np.median(winnings,axis=0),label="median")
	plt.plot(np.median(winnings,axis=0)-np.mean(winnings,axis=0),label="mean-STD")
	plt.plot(np.median(winnings,axis=0)+np.mean(winnings,axis=0),label="median+STD")
	plt.legend()
	plt.savefig("exp2b.png")

  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
