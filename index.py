import TextRepresenter as tr
import parser as par
import re
import numpy as np



class IndexSimple :

    def __init__(self,collection):


        self.collection = collection 
        self.len = len(self.collection)





        self.idx = {}
        self.inv = {}
        self.invnorm = {}
        self.doctfi = {}
        self.stemtfi = {}

        self.indexation()
        self.inv = self.inverseIndex(self.idx)
        self.normalise(self.inv)
        self.doctfi = self.TfIdf()
        self.stemtfi = self.inverseIndex(self.doctfi)


    def indexation(self):

        dictionnaire = {}
        p = tr.PorterStemmer()


        for id in self.collection.keys():

            document = self.collection[id]

            self.idx[id] = p.getTextRepresentation(document.getTexte()+document.getTitre())

    def inverseIndex(self,idxs):
        

        lexicon = {}
        inv = {}

        for new in idxs.values() :
            lexicon.update(new)



        for stem in lexicon :

            inv[stem] = {}

            for i in idxs.keys():
                if stem in idxs[i]:
                    inv[stem][i] = idxs[i][stem]
        
        return inv

    def normalise(self,idx):

        for id in idx.keys():

            tot = sum(idx[id].values())
            normalValues = map(lambda v : v/tot ,list(idx[id].values()))

            self.invnorm[id] = dict(zip(list(idx[id].keys()),normalValues))

    
    def Idf(self,stem):
        
        if stem in self.inv.keys():
            return np.log((1+self.len)/(1+len(self.inv[stem])))
        else :

            return np.log((1+self.len))


    def TfIdf(self):
        score = {}

        for document in self.idx.keys():
            score[document] = {}

            for stem, tot in self.idx[document].items():

                score[document][stem] = tot*self.Idf(stem)

        return score



    def getSize(self):
        return self.len

    def getIndex(self):
        return self.idx
    def getInverted(self):
        return dict(sorted(self.inv.items()))
    def getInvertedN(self):
        return dict(sorted(self.invnorm.items()))


    def getTfsForDoc(self,idx):

        return dict(sorted(self.idx[idx].items())) if idx in self.idx.keys() else {}

    def getTfIDFsForDoc(self,iddoc):
        return dict(sorted(self.doctfi[iddoc].items())) if iddoc in self.doctfi.keys() else {}
        

    def getTfsForStem(self,stem):
        return self.inv[stem] if stem in self.inv.keys() else {}

    def getTfIDFsForStem(self,stem):
        return self.stemtfi[stem] if stem in self.stemtfi.kyes() else {}

    def getStrDoc(self,iddoc):
        return self.collection[iddoc].getTexte() if iddoc in self.collection.keys() else None
        

    def toString(self):

        print(self.idx[1])
        print(('---------------------------------------------------','yellow'))
        print(self.inv['spurr'])
        print(('---------------------------------------------------','yellow'))
        print(self.invnorm['spurr'])
        print(('---------------------------------------------------','yellow'))
        print(self.doctfi[1])
        print(('---------------------------------------------------','yellow'))
        print(self.stemtfi['spurr'])









file = "data/cisi/cisi"
parse = par.Parser(file+".txt")

collection = parse.getRes()

idxSimple = IndexSimple (collection)

print(idxSimple.getStrDoc(1))

