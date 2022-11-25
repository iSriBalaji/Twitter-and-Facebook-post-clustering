import os
import csv
import pandas as pd

data_path = os.path.join(os.path.dirname(__file__),"Cleaned_Data.csv")
save_path = os.path.join(os.path.dirname(__file__),"Unique_Like_Followers.csv")
data = pd.read_csv(data_path)

print(data.columns)

data.drop_duplicates(subset=["pagename","Number of Likes","Number of Followers"], keep='first',inplace=True)

data.to_csv(save_path, index=False)

new_path =  os.path.join(os.path.dirname(__file__),"Unique_Like_Followers.csv")

ran = pd.read_csv(new_path)
print(ran.info)
print(ran.columns)
print(ran["Number of Likes"].max())
print(ran["Number of Followers"].max())
# 300,000  
# 500 5000 b1
# 5000 10000 b2
# 10000 50000 b3
# 50000 10000 b4
# 10000  30000 b5         300k+ ---> b6
st = ["300-500","500-5K","5K-10K","10K-50K","50K-100K","100K-300K","300K+"]
b1,b2,b3,b4,b5,b6,b7=0,0,0,0,0,0,0
for n,i in enumerate(ran["Number of Likes"]):
    try:
        a =int(i)
    except:
        continue
    if(a>=300 and a<500):
        b1+=1
    elif(a>=500 and a<5000):
        b2+=1
    elif(a>=5000 and a<10000):
        b3+=1
    elif(a>=10000 and a<50000):
        b4+=1
    elif(a>=50000 and a<100000):
        b5+=1
    elif(a>=100000 and a<300000):
        b6+=1
    else:
        b7+=1

l1 = [b1,b2,b3,b4,b5,b6,b7]   
print(l1)

b1,b2,b3,b4,b5,b6,b7=0,0,0,0,0,0,0
for n,i in enumerate(ran["Number of Followers"]):
    try:
        a =int(i)
    except:
        continue
    if(a>=300 and a<500):
        b1+=1
    elif(a>=500 and a<5000):
        b2+=1
    elif(a>=5000 and a<10000):
        b3+=1
    elif(a>=10000 and a<50000):
        b4+=1
    elif(a>=50000 and a<100000):
        b5+=1
    elif(a>=100000 and a<300000):
        b6+=1
    else:
        b7+=1

l2 = [b1,b2,b3,b4,b5,b6,b7]
print(l2)


save_path1 = os.path.join(os.path.dirname(__file__),"Muliple_Line_Graph.csv")
with open(save_path1, 'w') as f:
    for a,b,c in zip(st,l1,l2):
        f.write("%s,%s,%s\n"%(a,b,c))
