import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs={"leaf_size":1},bags=20,boost=False, verbose = False):
        self.learner = learner
        self.boost = boost
        self.verbose = verbose
        self.bags = bags

        self.learners = []        
        for i in range(0,bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return 'ssrishti3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        for learner in self.learners:
            #select random indices
            indices = np.random.choice(dataX.shape[0],dataX.shape[0])
            #select random entries
            learner.addEvidence(dataX[indices],dataY[indices])
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        ans_list = []
        for learner in self.learners:
            ans_list.append(learner.query(points))
        #averaging answer from each learner
        ans_list = np.mean(np.array(ans_list),axis=0)

        return ans_list

if __name__=="__main__":
    print('the secret clue if zzyzx')