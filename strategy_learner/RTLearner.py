import numpy as np
import random

class RTLearner(object):

    def __init__(self, leaf_size=5, verbose=False):

    	self.leaf_size = leaf_size
    	#initialize empty tree
    	self.tree = None

    def author(self):
    	return 'ssrishti3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        #build and save the model
        self.tree=self.build_tree(dataX,dataY)

    def build_tree(self,dataX,dataY):
    	#Quinlan algo
    	if dataX.shape[0]<=self.leaf_size:	  #only 1 row
    		return np.array([['Leaf',np.mean(dataY),-1,-1]])  #return [leaf,data.Y,NA,NA]

    	result = all(elem == dataY[0] for elem in dataY)   #if all elements in Y are same
    	if result:
    		return np.array([['Leaf',dataY[0],-1,-1]])   #return ['leaf,data.Y,NA,NA']

    	else:
    		#determine random best feature
    		best_feature = random.randint(0,dataX.shape[1]-1)

    		splitVal = np.median(dataX[:,best_feature])	#median of values in best feature column

    		#corner case
    		if splitVal==max(dataX[:,best_feature]):
    			return np.array([['Leaf',np.mean(dataY),-1,-1]])	#largest splitval value, no right tree

    		leftTree = self.build_tree(dataX[dataX[:,best_feature]<=splitVal],dataY[dataX[:,best_feature]<=splitVal])	#rows with val<=splitVal
    		rightTree = self.build_tree(dataX[dataX[:,best_feature]>splitVal],dataY[dataX[:,best_feature]>splitVal])    #rows with val>splitVal

    		root = np.array([[best_feature,splitVal,1,leftTree.shape[0]+1]])

    		app = np.append(root,leftTree,axis=0)
    		return np.append(app,rightTree,axis=0)

    def query(self,points):  #points=Xtest
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        Y = []  #to store regression values

        for i in range(0,points.shape[0]):
        	#loop through the tree for ans value
        	curr_row = 0
        	#loop while leaf node is reached
        	while(self.tree[curr_row,0]!='Leaf'):
        		feature = self.tree[curr_row,0]
        		splitVal = self.tree[curr_row,1]
        		if points[i,int(float(feature))] <= float(splitVal):  
        			#loop through left tree
        			curr_row = curr_row + int(float(self.tree[curr_row,2]))
        		else:
        			#loop through right tree
        			curr_row = curr_row + int(float(self.tree[curr_row,3]))
        	ans_i = self.tree[curr_row,1]   #y=splitval
        	Y.append(float(ans_i))

        return Y

if __name__=="__main__":
	print('the secret clue is zzyzx')