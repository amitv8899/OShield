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




serverUrl ="http://127.0.0.1:8000/" 

LocalDataPath = "C:\\Users\\AMIT\\Desktop\\studying\\workshop\\dataset\\my data\\data.xlsx"

fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier.sav'
fileLogisticRegression_model = 'LogisticRegression.sav'
db_file = 'C:\\Users\\AMIT\\workpalce\\django-proj\\sql.db'


#### help fun
def GetLocalData():
   return pd.read_excel(LocalDataPath)


def GetData():
   conn = create_connection(db_file)
   cur = conn.cursor()
   
   sql_query = pd.read_sql_query ('''SELECT * FROM frauddetection_data_charge''', conn)
   df = pd.DataFrame(sql_query, columns = ['id_Username', 'age', 'cityLiveIn','Gender','amount','hour_of_debit','time_of_debit','city_of_debit','credit_card_showed','is_fraud'])
   return df
   
def create_connection(db_file):
   conn = None
   try:
      conn = sqlite3.connect(db_file)
   except sqlite3.Error as e:
      print(e)

   return conn
   

def number_to_time(number):
   number = number*24
   left = number - int(number)
   left = (left)*60
   stringToConvert = str(str(int(number))+':'+str(int(left)))
   toReturn = datetime.strptime(stringToConvert, "%H:%M").time()
   return toReturn

def PrepareDF(df):
   X = df.drop(['is faurd','currency'] ,axis=1)
   Y = df['is faurd']
   dictGender = {
    'F':0,
    'M':1
    }

   dictTime = {
    'AM':0,
    'PM':1
    }
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
    pickle.dump(model,open(fileName,'wb'))

def Train(Tdata):## params = panada.df goal = to train model as in the colab
    

    X,Y = PrepareDF(Tdata)

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


def main():
    df =GetData()
    Train(df)
    
    
if __name__ == "__main__":
    main()










