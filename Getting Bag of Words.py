import os
import re
import csv
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


data_path = os.path.join(os.path.dirname(__file__),"Cleaned_Data.csv")
save_path = os.path.join(os.path.dirname(__file__),"Word_Cloud.csv")
save_path1 = os.path.join(os.path.dirname(__file__),"Unique_Cloud.csv")
data = pd.read_csv(data_path)

word = ""
word_ls = []
for n,i in enumerate(data["Content of Post"]):
    word+=i
    word_ls+=word_tokenize(i)
    if(n%1000==0):
        print("Creating Bag of Words...@",n)

print("----------------------------------Completed---------------------------------")
uniq_ls = list(set(word_ls))
print(len(word_ls))
unique_list = list(dict.fromkeys(word_ls))
print(len(unique_list))
print(len(uniq_ls))
    
fre = FreqDist()
ufre = FreqDist()
for i in word_ls:
    fre[i.capitalize()]+=1

for i in uniq_ls:
    ufre[i.capitalize()]+=1

print("Frequency Generated")

# pss=[]
# for key in fre.keys():
#     poss = nltk.pos_tag(key)
#     print(poss[0][1])
#     if(poss[0][1] not in pss):
#         pss.append(poss[0][1])

pss = ['NNP', 'PRP', 'DT', 'NN', 'VB', 'IN', 'CD', 'WRB', 'SYM', '$', 'RB']
with open(save_path, 'w') as f:
    for key in fre.keys():
        try:
            if(key[0].isdecimal() or key[1].isdecimal()):
                continue
        except:
            pass
        poss = nltk.pos_tag(key)
        if(poss[0][1] in ["NNP","NN","VB","NNS","NNPS","VBN"]):
            f.write("%s,%s\n"%(key,fre[key]))

print("Word Written")

with open(save_path1, 'w') as f:
    for key in ufre.keys():
        try:
            if(key[0].isdecimal() or key[1].isdecimal()):
                continue
        except:
            pass
        poss = nltk.pos_tag(key)
        if(poss[0][1] in ["NNP","NN","VB","NNS","NNPS","VBN"]):
            f.write("%s,%s\n"%(key,ufre[key]))

print("Written on CSV")