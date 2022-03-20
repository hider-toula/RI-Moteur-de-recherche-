import re
import numpy as np
#from abc import ABC, abstractmethod



class Document :

    def __init__(self,id,details={}):
        
        
        self.id = id
        if 'W' in details.keys(): self.texte = details['W']
        else: self.texte = ""
        if 'T' in details.keys(): self.titre = details['T']
        else: self.titre = ""
        if 'B' in details.keys(): self.date = details['B']
        else: self.date = ""
        if 'A' in details.keys(): self.auteur = details['A']
        else: self.auteur = ""
        if 'K' in details.keys(): self.mc = details['K']
        else: self.mc = ""
        if 'X' in details.keys(): self.liens = details['X']
        else: self.liens = []


    def snippet(self):

        print(('\n'+'id : ','white')+ (str(self.id),'green'))
        print(('title : ','white') + (self.titre,'green')+'\n')
        
        print((self.texte,"white"))

        print(('---------------------------------------------------','yellow'))
        
    def getID(self):
        return self.iddoc
    def getTexte(self):
        return self.texte
    def getTitre(self):
        return self.titre
    def getDate(self):
        return self.date
    def getAuteur(self):
        return self.auteur
    def getMc(self):
        return self.mc
    def getLiens(self):
        return self.liens
    
    def addTexte(self,texte):
        self.texte = texte
    def addTitre(self,titre):
        self.titre = titre
    def addDate(self,date):
        self.date = date
    def addAuteur(self,auteur):
        self.auteur = auteur
    def addMc(self,mc):
        self.mc = mc
    def addLiens(self,liens):
        self.liens = [liens]









class Parser():
    
    def __init__(self,path):
        self.collection = self.buildCollection(path)

    def buildCollection(self,path):

        collection = {}

        file = open(path,'r')

        lines = file.readlines()
        file.close()


        id = None
        balise = None


        for line in lines : 

            if(re.search("^[.]I",line)):
                id =  int(re.sub("\n","",line.split(" ")[1]))
                collection[id]={}
                continue

            if(re.search("^[.][A-Z]",line)):
                    
                    balise = line[1]
                    if balise == 'X': collection[id][balise] = []
                    else: collection[id][balise] = ""
                    continue


            if(line != "\n"):
                    
                    if balise == 'X':
                        collection[id][balise] += re.findall(r'\d+',line)
                    else: collection[id][balise] += re.sub(r'\n'," ",line)


        for document in collection.keys():

            collection[document]['T'] = re.sub(r'\+|\n'," ",collection[document]['T'].strip())
            if 'W' in collection[document].keys(): 
                collection[document]['W'] = re.sub(r'\r+'," ",collection[document]['W'].strip())
                collection[document]['W'] = re.sub(r'  '," ",collection[document]['W'].strip())
            collection[document] = Document(document,collection[document])
            

        return collection
        
    def getRes(self):
        return self.collection







