import os
import re
import nltk
import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from pywsd.utils import lemmatize_sentence,lemmatize
from dateutil.parser import parse

#getting all official country names
from country_list import countries_for_language
global coun
countries = dict(countries_for_language('en'))
coun = list(countries.values())
coun = list(map(lambda x:x.lower(),coun))
coun.remove("india")

data_path = os.path.join(os.path.dirname(__file__),"fb.csv")
save_path = os.path.join(os.path.dirname(__file__),"Cleaned_Data.csv")
data = pd.read_csv(data_path)
data.drop(["Unnamed: 0","reviewer","reviewerpage"],axis=1,inplace=True)
# Get the number of rows and columns 
rows = len(data.axes[0]) 
cols = len(data.axes[1]) 
  
# Print the number of rows and columns 
print("Number of Rows: " + str(rows)) 
print("Number of Columns: " + str(cols)) 
print("After Removing Duplicates")
data.drop_duplicates(subset ="content",inplace = True)
# Get the number of rows and columns 
rows = len(data.axes[0]) 
cols = len(data.axes[1]) 
  
# Print the number of rows and columns 
print("Number of Rows: " + str(rows)) 
print("Number of Columns: " + str(cols)) 
print(data.columns)
print(data.head)
# data["NameTag in Content"]=""
# data["HashTag in Content"]=""
# data["NameTag of Page"]=""
# data["Type/Organization"]=""

"""---------------------------------------------------FUNCTIONS TO CLEAN DATA-------------------------------------------------"""

#Remove unwanted characters in the text
def remove_pun(x):
    soup = BeautifulSoup(x, "html.parser")
    x = soup.get_text(separator=" ")
    x = re.sub('[^A-Za-z0-9]+', ' ', x)   
    return x

#Provide NameTag when n==0 and HashTag when n==1 from the String provided
def findTags(x,n):
    x = re.sub(r'http\S+', '', x)
    name_tag = []
    hash_tag = []
    x = x.split(" ")
    for x_v in range(len(x)):
        x_val = x[x_v]
        if "@" in x_val:
            a = remove_pun(x_val)
            name_tag.append(a)
        if "#" in x_val:
            a = remove_pun(x_val)
            hash_tag.append(a)
        if "@" in x_val or "#" in x_val:
            x[x_v] = ""
    if n==0:
        if name_tag ==[]:
            return None
        return " ".join(name_tag)
    if n==1:
        if hash_tag ==[]:
            return None
        return " ".join(hash_tag)

#Getting the Type or Org of the page
def groupOrg(st):
    ls=st.split("·")
    if(len(ls)==2):
        return(ls[1])
    elif(len(ls)==1):
        return(ls[0])
    print("More than 2")
    return None

def formatLikes(st,n):
    try:
        a = re.findall("[\d,]+",st)
        return(a[0].replace(',', ''))
    except TypeError:
        return("")

def removeMoji(x):
    soup = BeautifulSoup(x, "html.parser")
    x = soup.get_text(separator=" ")
    x = re.sub('[^A-Za-z0-9]+', ' ', x)  
    if not(x.isdecimal()):
        return(x.lower())

def clean_data(x):
    if x != False:
        for w in ["fashion","shopping","buy","marketing","sale","football","cricket","buying",\
                  "selling","srilanka","lanka","sri","shopping","entrepreneurs","bazaar",\
                  "business","dealing","marketing","trade","wholesale","promotion","enterprise","deal","purchase",\
                   "clearance","resale"
                  ]:
            x =  x.replace(w,"")
    return x

#if any other country were found it returns 1 else 0
def removeCountry(x):
    if x != False:
        for w in coun:
            if (x.find(w) != -1): 
                return(1)
    return(0)

def formatDate(dt,n):
    try:
        a = parse(dt)
        return(str(a.day)+"-"+str(a.month)+"-"+str(a.year))

    except:
        return None


def stopWords(x):
    tokens = word_tokenize(x)
    stopword_list = nltk.corpus.stopwords.words('english')
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_tokens = list(map(lambda x:lemmatize(x) ,filtered_tokens ))
    return(' '.join(map(str, filtered_tokens)))

def remNo(st):
    a = st.split()
    ls = list(filter(lambda x: not(x.isdecimal()),a))
    return(" ".join(ls))

def print_count(list_1,n):
    unique_list = list(dict.fromkeys(list_1))
    if n==0:
        return len(list_1)
    else:
        return len(unique_list)

"""---------------------------------------------------------------------------------------------------------------------------------"""
#Getting the type of Page and Nametag of Page
for n,i in enumerate(data["pagenametag"]):
    a = groupOrg(i)
    nt = findTags(i,0)
    if(n%1000==0):
        print("Getting Type...")
    if(a!=None):
            data.loc[data.index[n], "Type/Organization"] = a
    if(nt!=None):
            data.loc[data.index[n], "NameTag of Page"] = nt

#Extracting Name Tags and Hash Tags from Content Alone
for n,i in enumerate(data["content"]):
    a = findTags(i,0)
    b = findTags(i,1)
    if(n%1000==0):
        print("Extracting Hashtags...@",n)
    if(a!=None):
        data.loc[data.index[n], "NameTag in Content"] = a
    if(b!=None):
        data.loc[data.index[n], "HashTag in Content"] = b

data.drop(["pagenametag"],axis=1,inplace=True)

#Formatting No of Likes
for n,i in enumerate(data["numberoflikes"]):
    a = formatLikes(i,n)
    if(n%1000==0):
        print("Cleaning Likes...@",n)
    if(a!=None):
            data.loc[data.index[n], "Number of Likes"] = a

#Formatting No of Followers
for n,i in enumerate(data["numberoffollowers"]):
    a = formatLikes(i,n)
    if(n%1000==0):
        print("Cleaning Followers...@",n)
    if(a!=None):
            data.loc[data.index[n], "Number of Followers"] = a


data.drop(["numberoflikes","numberoffollowers"],axis=1,inplace=True)


#Formatting Date
for n,i in enumerate(data["reviewdate"]):
    a =formatDate(i,n)
    if(n%1000==0):
        print("Formatting Date...@",n)
    if(a!=None):
        data.loc[data.index[n], "Posted Date"] = a


# Cleaning the Content
rls=[]
cn=0
data["content"] = data["content"].map(lambda x:x.replace("See more",""))
data['content'] = data['content'].apply(lambda x: re.sub('https?://[A-Za-z0-9./]+','',x))
for n,i in enumerate(data["content"]):
    a = removeMoji(i)
    b = clean_data(a)
    c =stopWords(b)
    d = remNo(c)
    e = removeCountry(d)
    if(n%1000==0):
        print("Cleaning Content...@ ",n)
    data.loc[data.index[n], "Content of Post"] = d
    if(d=="" or e==1):
        if(e==1):
            cn+=1
        print("Empty value")
        rls.append(n)
print("Empty string len = ",len(rls))
print("Other Country Removed = ",cn)
print("Removing unwanted Datas")
for n in rls:
    data.drop(axis=0,index=n,inplace=True)

#Getting Label from the data
for n,i in enumerate(data["t_file"]):
    a = i.split("_")
    if(n%1000==0):
        print("Getting Label...@",n)
    data.loc[data.index[n], "Label"] = a[-2]

data['Tokens'] = data.apply(lambda row: nltk.word_tokenize(row['Content of Post']), axis=1)
data["Word Count"] = data["Tokens"].map(lambda x:print_count(x,0))
data["Unique Words"] = data["Tokens"].map(lambda x:print_count(x,1))

data.drop(["content","reviewdate","t_file"],axis=1,inplace=True)
print(data.columns)
print(data.sample(20))
data.to_csv(save_path, index=False)
#print(a)
