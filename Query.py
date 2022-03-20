import re
import numpy as np

class Query(object):
    def __init__(self,idquery):
        self.idquery = idquery
        self.texte = ""
        self.pertinents = [] 
        
    def showQuery(self):
        print(self.idquery,"\n",self.texte)
    
    def getIdQuery(self):
        return self.idquery
    def getTexte(self):
        return self.texte
    def getPertinents(self):
        return self.pertinents
    def addTexte(self,texte):
        self.texte += texte
    def addPertinents(self,pertinent):
        self.pertinents += [pertinent]
        
class QueryParser(object):
    def __init__(self,queries,pertinents):
        self.fquery = queries 
        self.fperti = pertinents 
        self.qoll = self.parsing()  
        
    def parsing(self):

        qoll = {}
        with open(self.fquery,"r") as f:
            balise = None
            idq = None
            for line in f.readlines():
                if(re.search("^[.]I",line)):
                    idq = int(re.sub("\n","",line.split(" ")[1]))
                    qoll[idq] = Query(idq) 
                    continue 
                if(re.search("^[.][A-Z]",line)):
                    balise = line[1]
                    continue
                if(line != "\n" and balise == 'W'):
                    qoll[idq].addTexte(re.sub("\n"," ",line))  
        with open(self.fperti,"r") as f:
            for line in f.readlines():
                idq, perti = re.findall(r'\d+',line)[0:2]
                if idq[0]=='0': idq = idq[1:]
                idq = int(idq)
                qoll[idq].addPertinents(int(perti))
        return qoll
    
    def getQoll(self):
        return self.qoll