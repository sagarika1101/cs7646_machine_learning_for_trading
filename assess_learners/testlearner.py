"""                                                               
Test a learner.  (c) 2015 Tucker Balch                                                                
                                                                
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
"""                                                               
                                                                
import numpy as np                                                                
import math                                                               
import LinRegLearner as lrl                                                               
import sys     
from numpy import genfromtxt 
import DTLearner as dt  
import matplotlib.pyplot as plt   
import BagLearner as bg   
import time  
import RTLearner as rt                                               
                                                                
if __name__=="__main__":                                                                
    if len(sys.argv) != 2:                                                                
        print("Usage: python testlearner.py <filename>")                                                                
        sys.exit(1)                                                               
    #inf = open(sys.argv[1])                                                               
    #data = np.array([list(map(float,s.strip().split(','))) for s in inf.readlines()])      

    data = genfromtxt(sys.argv[1], delimiter=',')  
    data = data[1:,1:]  #remove date and header 
    #print(data)                                                    
                                                                
    # compute how much of the data is training and testing                                                                
    train_rows = int(0.6* data.shape[0])                                                                
    test_rows = data.shape[0] - train_rows                                                                
                                                                
    # separate out training and testing data                                                                
    trainX = data[:train_rows,0:-1]                                                               
    trainY = data[:train_rows,-1]                                                               
    testX = data[train_rows:,0:-1]                                                                
    testY = data[train_rows:,-1]                                                                
                                                                
    #print(f"{testX.shape}")                                                               
    #print(f"{testY.shape}")    

    
    #Q1                                                                  
    # create a learner and train it  
    #testing for leaf_size 1-20
    in_sample_RMSE = []
    out_sample_RMSE = []
    for leaf_size in range(1,21):         
      #print('iteration' + str(leaf_size))                                                    
      learner = dt.DTLearner(leaf_size = leaf_size,verbose = True) # create a LinRegLearner                                                                
      learner.addEvidence(trainX, trainY) # train it                                                                
      #print(learner.author())                                                               
                                                                  
      # evaluate in sample                                                                
      predY = learner.query(trainX) # get the predictions                                                               
      rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])     
      in_sample_RMSE.append(rmse)                                                          
      #print()                                                               
      #print("In sample results")                                                                
      #print(f"RMSE: {rmse}")                                                                
      c = np.corrcoef(predY, y=trainY)                                                                
      #print(f"corr: {c[0,1]}")                                                                
                                                                  
      # evaluate out of sample                                                                
      predY = learner.query(testX) # get the predictions                                                                
      rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])   
      out_sample_RMSE.append(rmse)                                                            
      #print()                                                               
      #print("Out of sample results")                                                                
      #print(f"RMSE: {rmse}")                                                                
      c = np.corrcoef(predY, y=testY)                                                               
      #print(f"corr: {c[0,1]}")       

    #plotting
    fig,ax=plt.subplots()
    plt.title("RMSE vs. Leaf Size")
    plt.xlabel("Leaf Size")
    #plt.xlim(1,20)
    plt.ylabel("RMSE")
    #plt.ylim(0,0.008)   
    plt.plot(in_sample_RMSE,label='In Sample RMSE')
    plt.plot(out_sample_RMSE,label = 'Out Sample RMSE')
    plt.legend()
    plt.savefig("Q1.png")   
     

    #Q2                                                               
    # create a learner and train it  
    #testing for leaf_size 1-20
    in_sample_RMSE = []
    out_sample_RMSE = []
    for leaf_size in range(1,21):         
      #print('iteration' + str(leaf_size))                                                    
      learner = bg.BagLearner(learner = dt.DTLearner, kwargs = {'leaf_size':leaf_size}, bags = 10, boost = False, verbose = True)                                                                 
      learner.addEvidence(trainX, trainY) # train it                                                                
      #print(learner.author())                                                               
                                                                  
      # evaluate in sample                                                                
      predY = learner.query(trainX) # get the predictions                                                               
      rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])     
      in_sample_RMSE.append(rmse)                                                          
      #print()                                                               
      #print("In sample results")                                                                
      #print(f"RMSE: {rmse}")                                                                
      c = np.corrcoef(predY, y=trainY)                                                                
      #print(f"corr: {c[0,1]}")                                                                
                                                                  
      # evaluate out of sample                                                                
      predY = learner.query(testX) # get the predictions                                                                
      rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])   
      out_sample_RMSE.append(rmse)                                                            
      #print()                                                               
      #print("Out of sample results")                                                                
      #print(f"RMSE: {rmse}")                                                                
      c = np.corrcoef(predY, y=testY)                                                               
      #print(f"corr: {c[0,1]}")       

    #plotting
    fig,ax=plt.subplots()
    plt.title("RMSE vs. Leaf Size")
    plt.xlabel("Leaf Size")
    #plt.xlim(1,20)
    plt.ylabel("RMSE")
    #plt.ylim(0,0.008)   
    plt.plot(in_sample_RMSE,label='In Sample RMSE')
    plt.plot(out_sample_RMSE,label = 'Out Sample RMSE')
    plt.legend()
    plt.savefig("Q2.png")      

    

    #Q3                                                              
    # create a learner and train it  
    #a) measuring training time
    #taking 10-100% of training set
    time_DT = []
    time_RT = []
    for i in range(1,train_rows):
      temp_trainX = trainX[:i,:]
      temp_trainY = trainY[:i]

      #DTLearner                                                  
      learner = dt.DTLearner(leaf_size = 1, verbose = True)   
      start_time = time.time()                                                              
      learner.addEvidence(temp_trainX, temp_trainY) # train it   
      end_time = time.time()                                                             
      #print(learner.author())                                                               
      diff_DT = end_time - start_time       
      time_DT.append(diff_DT)                                                     
      
      #RTLearner  
      learner = rt.RTLearner(leaf_size = 1, verbose = True)   
      start_time = time.time()                                                              
      learner.addEvidence(temp_trainX, temp_trainY) # train it   
      end_time = time.time()                                                             
      #print(learner.author())                                                               
      diff_RT = end_time - start_time  
      time_RT.append(diff_RT)   

    #print(time_DT)
    #print(time_RT)

    #plotting
    fig,ax=plt.subplots()
    plt.title("Training time vs. Training Data Size")
    plt.xlabel("Training data size")
    #xlim=ax.get_xlim()
    #factor=0.1
    #new_xlim=(xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor) 
    #ax.set_xlim(new_xlim)
    plt.ylabel("Training Time (s)")
    #plt.ylim(0,0.01)   
    plt.plot(time_DT,label='DTLearner')
    plt.plot(time_RT,label = 'RTLearner')
    plt.legend()
    plt.savefig("Q3.a.png")             

    #b) measuring tree size
    #taking 10-100% of training set
    size_DT = []
    size_RT = []
    for i in range(1,train_rows):
      temp_trainX = trainX[:i,:]
      temp_trainY = trainY[:i]

      #DTLearner                                                  
      learner = dt.DTLearner(leaf_size = 1, verbose = True)   
      learner.addEvidence(temp_trainX, temp_trainY) # train it   
      #print(learner.author())                                                               
      size_DT.append(learner.tree.shape[0])                                                     
      
      #RTLearner  
      learner = rt.RTLearner(leaf_size = 1, verbose = True)   
      learner.addEvidence(temp_trainX, temp_trainY) # train it   
      #print(learner.author())                                                               
      size_RT.append(learner.tree.shape[0])   

    #print(size_DT)
    #print(size_RT)

    #plotting
    fig,ax=plt.subplots()
    plt.title("Tree Size vs. Training Data Size")
    plt.xlabel("Training data size")
    #xlim=ax.get_xlim()
    #factor=0.1
    #new_xlim=(xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor) 
    #ax.set_xlim(new_xlim)
    plt.ylabel("Tree size")
    #plt.ylim(0,0.01)   
    plt.plot(size_DT,label='DTLearner')
    plt.plot(size_RT,label = 'RTLearner')
    plt.legend()
    plt.savefig("Q3.b.png")                                
