import numpy as np
import TextRepresenter as tr

class Weighter():
    def __init__(self,refindex):
   

        self.ref = refindex
        self.inds = refindex.getIndex()
        self.inv = refindex.getInverted()
    
    def getWeightsForDoc(self,iddoc):
        pass
    
    def getWeightsForStem(self,stem):
        pass
    
    def getWeightsForQuery(self,query):
        pass



class Weighter1(Weighter):


    def __init__(self,refindex):
        super().__init__(refindex)

    def getWeightsForDoc(self,iddoc):
        """output: {word: nb_occ}"""
        return self.ref.getTfsForDoc(iddoc)
    def getWeightsForStem(self,stem):
        """output: {iddoc des docs contenant stem: nb_occurences}"""
        return self.ref.getTfsForStem(stem)
    def getWeightsForQuery(self,query):
        """output: {word: 1}"""
        p = tr.PorterStemmer()
        qindex = p.getTextRepresentation(query)
        return dict(zip(qindex.keys(),np.ones(len(qindex))))


class Weighter5(Weighter):
   
   
    def __init__(self,Index):
        super().__init__(Index)
    def getWeightsForDoc(self,iddoc):
        """output: {word: (1+log(nb_occ))*idf}"""
        weights = {stem:((1+np.log(tf))*self.ref.computeIdf(stem)) for stem, tf in self.inds[iddoc].items()}
        return weights

    def getWeightsForStem(self,stem):
        """output: {iddoc des docs contenant word: (1+log(nb_occ))*idf}"""
        if stem in self.inv.keys():
            idf = self.ref.computeIdf(stem)
            return {source:((1+np.log(tf))*idf) for source, tf in self.inv[stem].items()}
        return {}        
    def getWeightsForQuery(self,query):
        """output: {word: (1+log(nb_occ))*idf}"""
        p = tr.PorterStemmer()
        quind = p.getTextRepresentation(query)
        weights = {stem:((1+np.log(quind[stem]))*self.ref.computeIdf(stem)) for stem in quind.keys()}
        return weights



class Weighter2(Weighter):


    def __init__(self,refindex):
        super().__init__(refindex)
    def getWeightsForDoc(self,iddoc):
        """output: {word: nb_occ}"""
        return self.ref.getTfsForDoc(iddoc)
    def getWeightsForStem(self,stem):
        """output: {iddoc des docs contenant word: nb_occurences}"""
        return self.ref.getTfsForStem(stem)
    def getWeightsForQuery(self,query):
        """output: {word: nb_occurences}"""
        p = tr.PorterStemmer()
        return p.getTextRepresentation(query)



class Weighter3(Weighter):
 

    def __init__(self,refindex):
        super().__init__(refindex)
    def getWeightsForDoc(self,iddoc):
        """output: {word: nb_occ}"""
        return self.ref.getTfsForDoc(iddoc)
    def getWeightsForStem(self,stem):
        """output: {iddoc des docs contenant word: nb_occurences}"""
        return self.ref.getTfsForStem(stem)
    def getWeightsForQuery(self,query):
        """output: {word: idf}"""
        p = tr.PorterStemmer()
        weights = {stem:self.ref.computeIdf(stem) for stem in p.getTextRepresentation(query).keys()}
        return weights


class Weighter4(Weighter):
    
    def __init__(self,refindex):
        super().__init__(refindex)
    def getWeightsForDoc(self,iddoc):
        """output: {word: 1+log(nb_occ)}"""
        weights = {stem:(1+np.log(tf)) for stem, tf in self.inds[iddoc].items()}
        return weights
    def getWeightsForStem(self,stem):
        """output: {iddoc des docs contenant word: 1+log(nb_occ)}"""
        if stem in self.inv.keys():
            return {source:(1+np.log(tf)) for source, tf in self.inv[stem].items()}
        return {}
    def getWeightsForQuery(self,query):
        """output: {word: idf}"""
        p = tr.PorterStemmer()
        weights = {stem:self.ref.computeIdf(stem) for stem in p.getTextRepresentation(query).keys()}
        return weights