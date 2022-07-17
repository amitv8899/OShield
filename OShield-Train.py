from cmath import e
import numpy as np
import pandas as pd
import datetime

#fix data
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split


# Classifier Libraries / train
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import collections
from sklearn.model_selection import cross_val_score
#extra train
from sklearn.model_selection import GridSearchCV

#save models
import pickle
#save models
import pickle
# server
import requests
import urllib.request
import base64
import sqlite3

#static vals:
serverUrl ="http://127.0.0.1:8000/" 
LocalDataPath = "C:\\Users\\AMIT\\Desktop\\studying\\workshop\\dataset\\my data\\data.xlsx"
fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier.sav'
fileLogisticRegression_model = 'LogisticRegression.sav'
db_file = 'C:\\Users\\AMIT\\workpalce\\django-proj\\db.sqlit3'

cl = ["id","age","live city","gender","amount","hour of debit","time of debit","city of debit","credit card showed","is fraud"
]


#### help fun
def GetLocalData():
   return pd.read_excel(LocalDataPath)


def GetData()-> pd.DataFrame:
   conn = create_connection(db_file)
   cur = conn.cursor()
   sql_query = pd.read_sql_query ('''SELECT * FROM frauddetection_data_charge''', conn)
   df = pd.DataFrame(sql_query, columns = ['id_User', 'age', 'cityLiveIn','gender','amount','hour_of_debit','time_of_debit','city_of_debit','credit_card_showed','is_fraud'])
   return df
   
def create_connection(db_file):
   try:
      conn = sqlite3.connect(db_file)
   except sqlite3.Error as e:
      print(e)
      return None

   return conn
def time_to_number(time: datetime.time) -> int:
   strh = time.strftime("%H")
   strm = time.strftime("%M")
   time_num = (int(strh)*100) + int(strm)

   return time_num
   
   
   


def PrepareDF(df,is_train):
   Y = None
   if is_train:
      ## split to x and y
       X = df.drop(['is fraud'] ,axis=1)
       Y = df['is faurd']

   # replace F and M to 1 and 0
   dictGender = {
    'F':0,
    'M':1,
    'f':0,
    'm':1
    }
    # replace am or pm to 1 and 0
   dictTime = {
    'AM':0,
    'PM':1,
    'am':0,
    'pm':1
    }
    # replace cities to number
   NumberOfCities = 1
   dictCities = {}
   CitiesArr = X[['live city','city of debit']].to_numpy()

   for Lc,Dc in CitiesArr :
       if Lc not in dictCities:
          dictCities[Lc] = NumberOfCities
          NumberOfCities = NumberOfCities + 1
       if Dc not in dictCities:
          dictCities[Dc] = NumberOfCities
          NumberOfCities = NumberOfCities + 1
    

   new_x = X.copy()
   new_x.replace({"gender":dictGender,"time of debit":dictTime,'live city':dictCities,'city of debit':dictCities},inplace=True)
   new_x["hour_of_debit"] = new_x["hour_of_debit"].apply(time_to_number)
        
   return new_x,Y
## main fun
def LogisticRegression_H():
   return LogisticRegression()

def KNeighborsClassifier_H():
   return KNeighborsClassifier()

def DecisionTreeClassifier_H():
   return DecisionTreeClassifier()

def SaveAllModels(*argv):# known number of models - *args
    for arg in argv:
        if type(arg) is KNeighborsClassifier:
            SaveModel(arg,fileKNearest_model)
        elif type(arg) is DecisionTreeClassifier:
            SaveModel(arg,fileDecisionTreeClassifier_model)
        elif type(arg) is LogisticRegression:
            SaveModel(arg,fileDecisionTreeClassifier_model)        

def SaveModel(model,fileName):
   try:
     pickle.dump(model,open(fileName,'wb'))
   except OSError as err:
      print("OS error: {0}".format(err))
      

def Train(Tdata : pd.DataFrame):## params = panada.df goal = to train model as in the colab
    

    X,Y = PrepareDF(Tdata,True)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    X_train = X_train.values
    X_test = X_test.values
    Y_train = Y_train.values
    Y_test = Y_test.values

    LogisticRegression_model =  LogisticRegression_H()
    KNeighborsClassifier_model = KNeighborsClassifier_H()
    DecisionTreeClassifier_model = DecisionTreeClassifier_H()

    ##LogisticRegression_model.fit(X_train, Y_train)
    KNeighborsClassifier_model.fit(X_train, Y_train)
    DecisionTreeClassifier_model.fit(X_train, Y_train)

    
    SaveAllModels(DecisionTreeClassifier_model,KNeighborsClassifier_model)
    
    return


#delete
def Prediction(KNearest_model,DecisionTreeClassifier_model,data):## input 2 models and data to predict -> uotput us a list of the rows that could be fraud
    KNearest_model_P = KNearest_model.predict(data.to_numpy())
    DecisionTreeClassifier_model_P = DecisionTreeClassifier_model.predict(data.to_numpy())
    fruad = [l1+l2 for l1,l2 in zip(DecisionTreeClassifier_model_P,KNearest_model_P)]
    return [i for i,val  in enumerate(fruad) if val > 1]
 
def LoadModels():
    try:
       KNearest_model = pickle.load(open(fileKNearest_model, 'rb'))
       DecisionTreeClassifier_model = pickle.load(open(fileDecisionTreeClassifier_model, 'rb'))
       ##LogisticRegression_model = pickle.load(open(fileLogisticRegression_model, 'rb'))
    except OSError as err:
       print("OS error: {0}".format(err))
       return None,None

    return KNearest_model,DecisionTreeClassifier_model 


def main():

   df =GetData()
   Train(df)
   
   

   
   


   
         


  
    
    
if __name__ == "__main__":
    main()







