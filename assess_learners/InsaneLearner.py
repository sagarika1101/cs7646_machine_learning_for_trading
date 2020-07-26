import numpy as np
import BagLearner as bg
import LinRegLearner as lrl

class InsaneLearner(object):

    def __init__(self,verbose = False):
        
        self.learners=[]
        for i in range(0,20):
            self.learners.append(bg.BagLearner(lrl.LinRegLearner,kwargs={},bags=20))

    def author(self):
        return 'ssrishti3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        #add data for each learner
        for learner in self.learners:
            learner.addEvidence(dataX,dataY)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        #query answer for each learner
        ans_list = []
        for learner in self.learners:
            ans = learner.query(points)
            ans_list.append(ans)
        #averaging answer from each learner
        ans_list = np.mean(np.array(ans_list),axis=0)

        return ans_list

if __name__=="__main__":
    print('the secret clue is zzyzx')