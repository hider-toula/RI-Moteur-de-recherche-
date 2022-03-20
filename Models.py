
import TextRepresenter as tr
import numpy as np



class IRModel():
    def __init__(self,refindex):

        self.ref = refindex  
        self.inds = refindex.getIndex()
        self.inv = refindex.getInverted()
        self.invn = refindex.getInvertedN()
    
    def getScores(self,query):

        pass
    
    def getRanking(self,query):

        docs_scores = self.getScores(query)
        return [(k,v) for k,v in sorted(docs_scores.items(), key=lambda item: item[1], reverse=True) if v!=0]



class Vectoriel(IRModel):

    def __init__(self,refindex,refweighter,normalized=False):

        super().__init__(refindex)
        self.weightype = refweighter 
        self.normalized = normalized 
        if self.normalized:

            self.normDs = {source:np.sqrt(np.sum(np.power(list(self.weightype.getWeightsForDoc(source).values()),2))) for source in self.inds.keys()}
    def getScores(self, query):

        qweights = self.weightype.getWeightsForQuery(query)
        qstems = qweights.keys()

        scores = dict.fromkeys(range(1,self.ref.getSize()[0]+1),0)
        if not self.normalized:

            for stem in qstems:
                sweights = self.weightype.getWeightsForStem(stem)
                for source, o in sweights.items():
                    scores[source] += o*qweights[stem]
        else:

            normQ = np.sqrt(np.sum(np.power(list(qweights.values()),2)))
            for stem in qstems:
                sweights = self.weightype.getWeightsForStem(stem)
                for source, o in sweights.items():
                    scores[source] += (o*qweights[stem])/(normQ+self.normDs[source])
        return scores


class ModeleLangue(IRModel):
    def __init__(self,refindex,l=0.8):

        super().__init__(refindex)
        self.l = l
        
    def getScores(self,query):

        p = tr.PorterStemmer()
        qstems = p.getTextRepresentation(query).keys()          
        scores = {}


        for stem in qstems:
            pcoll = sum(self.inv[stem].values())/self.ref.getSize()[2] if stem in self.inv.keys() else 0

            for source in self.inds.keys():
                pdoc = self.invn[stem][source] if stem in self.inds[source].keys() else 0

                if ((1-self.l)*pdoc+self.l*pcoll)>0:
                    scores[source] = scores.get(source,0)+np.log((1-self.l)*pdoc+self.l*pcoll)
        return scores                 


class Okapi(IRModel):
    def __init__(self,refindex,k1=1.2,b=0.75):

        super().__init__(refindex)
        self.k1 = k1
        self.b = b
        self.avgdl = np.mean([sum(self.inds[source].values()) for source in self.inds.keys()])
        
    def getScores(self,query):
        p = tr.PorterStemmer()
        qstems = p.getTextRepresentation(query).keys()
        scores = dict.fromkeys(range(1,self.ref.getSize()[0]+1),0)
        lendocs = {source:sum(self.inds[source].values()) for source in self.inds.keys()}
        for stem in qstems:
            idf = self.ref.computeIdf(stem)
            for source in self.inds.keys():
                if stem in self.inds[source].keys():
                    tf = self.inds[source][stem]
                    scores[source] += idf*(tf/(tf+self.k1*(1-self.b+self.b*(lendocs[source]/self.avgdl))))
        return scores