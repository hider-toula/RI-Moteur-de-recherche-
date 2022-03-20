from parser import Parser, Document
from index import IndexSimple
from Weighter import Weighter1, Weighter2, Weighter3, Weighter4, Weighter5
from Models import Vectoriel, ModeleLangue, Okapi
from Query import QueryParser
from Metric import Precision, Rappel, FMesure, AvgPrecision, ReciprocalRank, NDCG
from Eval import EvalIRModel
import numpy as np
import pandas as pd


# Phase de test. 
file = "data/cisi/cisi"
# file = "data/cacm/cacm"

print("Phase de test sur la collection CISI.\n\n                        ***")

# --------------------------------------------------------------------------- parsing + indexation ---------------------------

print("\n                     PARSER ///////////////////////////////////////////////////////////////////////////////////////")
print("\nParser la collection et afficher les trois premiers documents, puis le tout dernier.")
parse = Parser(file+".txt")
coll = parse.getResult()
print("\nAffichage de la collection. \n")
for document in list(coll.keys())[:3]:
     coll[document].snippet()
fin = 2460 
coll[fin].snippet()




indexcoll = IndexerSimple(coll)
print("\nTaille de la collection : ", indexcoll.getSize()[0])
print("\nScoring du dernier document : ", indexcoll.getTfIDFsForDoc(fin))
print("\nListe partielle du vocabulaire : ", list((indexcoll.getInverted()).keys())[8000:9000])
     

w = Weighter5(indexcoll)
v = Vectoriel(indexcoll,w,True) # Score cosinus.
m = ModeleLangue(indexcoll,0.1)
# Valeur cacm : 0.9
# Okapi BM25 *AVEC OPTIMISATION CISI*, cf. bonus en annexe.
o = Okapi(indexcoll,1.8,0.88) 
# Valeurs cacm : 
mods = {"Vectoriel":v, "Jelinek":m, "Okapi":o}

req = "The present study is a history of the DEWEY Decimal Classification.abroad" # version cisi
# req = "Computer Language : dramatic speed shallow or deep" # version cacm


print(m.getRanking(req)[0:20])

#print(list(o.getScores(req).items())[0:20],"\n")
print(o.getRanking(req)[0:20])

print(indexcoll.getTfsForDoc(1))
print(indexcoll.getTfsForDoc(260))
print(indexcoll.getTfsForDoc(354))
print(indexcoll.getTfsForDoc(282))
print(indexcoll.getTfsForDoc(1152))
print(indexcoll.getTfsForDoc(2287))




qp = QueryParser(file+".qry",file+".rel")
queries = qp.getQoll()

for q in list(queries.values())[37:42]:
    q.showQuery()


p = 50 
prec = Precision(p)
rapp = Rappel(p)
fmes = FMesure(p)
avgP = AvgPrecision()
rank = ReciprocalRank()
ndcg = NDCG(p)

mets = {"Precision":prec, "Recall":rapp, "FScore":fmes, "AvgPrecision": avgP, "RecipRank": rank, "NDCG":ndcg}


e = EvalIRModel(mods,mets,queries)
e.finalEv()

df = pd.DataFrame(e.evalAll())


modeleX = 'Okapi'  
modeleY = 'Vectoriel'
mesure = 'RecipRank'

X = np.array([e.evalSimple(idq,modeleX,mesure) for idq in queries.keys()])
Y = np.array([e.evalSimple(idq,modeleY,mesure) for idq in queries.keys()])

z, cv, res = e.tTest(X,Y,0.05)
print("t-test value: {}".format(z))
print("critical value: {}".format(cv))
print("Selon {}, {} et {} sont-ils similaires ? {}".format(mesure, modeleX, modeleY, res))

