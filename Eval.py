import numpy as np
import scipy.stats
import pandas

class EvalIRModel(object):
    def __init__(self,dictModels,dictMetrics,queries):
        self.dictModels = dictModels 
        self.dictMetrics = dictMetrics 
        self.queries = queries 
        
    def evalSimple(self,idq,mod,met):

        liste = self.dictModels[mod].getRanking(self.queries[idq].getTexte())
        return self.dictMetrics[met].evalQuery(liste,self.queries[idq])
    
    def evalSingleQuery(self,idq):
        evaluate = {}
        for met in self.dictMetrics.keys():
            evaluate[met] = {mod:self.evalSimple(idq,mod,met) for mod in self.dictModels.keys()}
        return evaluate
    
    def evalSingleComb(self,mod,met):

        evaluate = np.array([self.evalSimple(idq,mod,met) for idq in self.queries.keys()])
        return (np.mean(evaluate),np.std(evaluate))
    
    def evalAll(self):

        evaluate = {}
        for met in self.dictMetrics.keys():
            evaluate[met] = {}
            for mod in self.dictModels.keys():
                underev = np.array([self.evalSimple(idq,mod,met) for idq in self.queries.keys()])
                evaluate[met][mod] = (np.round(np.mean(underev)*100,3),np.round(np.std(underev)*100,3))
        return evaluate
    
    def tTest(self,X,Y,alpha):

        n = len(X)
        meanX = np.mean(X) 
        meanY = np.mean(Y)
        sX = np.sum((X-meanX)**2)/(n-1)
        sY = np.sum((Y-meanY)**2)/(n-1)
        z = (meanX-meanY)/(np.sqrt((sX+sY)/n)) 
        df = 2*n - 2 
        cv = scipy.stats.t.ppf(1.0 - alpha/2, df) 
        return z, cv, np.abs(z) <= cv
    
    def finalEv(self): 
        
        whole = self.evalAll()
        whole = pandas.DataFrame.from_dict(whole)
        print(whole)
        return whole