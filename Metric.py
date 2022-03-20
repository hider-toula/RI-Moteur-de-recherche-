
import numpy as np

class EvalMesure():
    def __init__(self):
        pass
    def evalQuery(self,liste,Query):
        pass

class Precision(EvalMesure):
    def __init__(self,rang):
        super().__init__()
        self.rang = rang 
    def evalQuery(self,liste,req):
        tentative = set([source for source, score in liste[:self.rang]])
        reference = set(req.getPertinents())
        truepos = len(tentative.intersection(reference)) 
        if len(tentative) == 0: return 0
        return truepos/len(tentative)
    
class Rappel(EvalMesure):
    def __init__(self,rang):
        super().__init__()
        self.rang = rang 
    def evalQuery(self,liste,req):
        tentative = set([source for source, score in liste[:self.rang]])
        reference = set(req.getPertinents())
        truepos = len(tentative.intersection(reference)) 
        if len(reference) == 0: return 1
        return truepos/len(reference) 
    
class FMesure(EvalMesure):
    def __init__(self,rang,beta=1):
        super().__init__()
        self.rang = rang 
        self.beta = beta 
    def evalQuery(self,liste,req):
        tentative = set([source for source, score in liste[:self.rang]])
        reference = set(req.getPertinents())
        truepos = len(tentative.intersection(reference))
        P = truepos/len(tentative) if len(tentative)!=0 else 0 
        R = truepos/len(reference) if len(reference)!=0 else 0 
        if (P+R) != 0: return (1+self.beta**2) * (P*R)/(self.beta**2*(P+R))
        return 0
    
class AvgPrecision(EvalMesure):
    def __init__(self):
        super().__init__()
    def evalQuery(self,liste,req):
        reference = req.getPertinents()
        if len(reference) == 0: return 0
        pertinence = np.array([1 if source in reference else 0 for source,score in liste])
        somme = 0
        for k in np.where(pertinence==1)[0]+1: # (ajustement des indices) 
            somme += sum(pertinence[:k])/k
        return somme/len(reference)

class ReciprocalRank(EvalMesure):
    def __init__(self):
        super().__init__()
    def evalQuery(self,liste,req):
        reference = req.getPertinents()
        somme = 0
        for i in range(len(liste)):
            if liste[i][0] in reference:
                somme = i+1 
                break
        if somme==0: return 0
        else: return 1/somme 
    
class NDCG(EvalMesure):

    def __init__(self,rang):
        super().__init__()
        self.rang = rang 
    def evalQuery(self,liste,req):
        if len(liste) == 0: return 0
        reference = req.getPertinents()
        p = min(len(liste),self.rang)
        pertinence = np.array([1 if source in reference else 0 for source, score in liste[:p]])
        p2 = min(len(reference),self.rang)
        dcg = pertinence[0] + np.sum(pertinence[1:]/np.log2(range(2,p+1)))
        idcg = np.sum(np.ones(p2)/np.hstack((np.array([1]),np.log2(range(2,p2+1)))))
        if idcg == 0: return 0
        return dcg/idcg
