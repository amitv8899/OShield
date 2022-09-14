## good
#handle data
#check git!
from typing import Dict, List
import numpy as np
import pandas as pd
import datetime
import geopy.distance as geoD

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
import os
from pathlib import Path

# server
import sqlite3

#static vals:
serverUrl ="http://127.0.0.1:8000/"
LocalDataPath = "C:\\Users\\AMIT\\Desktop\\studying\\workshop\\dataset\\my data\\data.xlsx"
fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier_model.sav'
fileLogisticRegression_model = 'LogisticRegression_model.sav'
db_file = 'C:\\Users\\AMIT\\workpalce\\django-proj\\db.sqlite3'
cl = ['user_id', 'age', 'cityLiveIn','gender','amount',
   'hour_of_debit','time_of_debit','date_of_debit','city_of_debit','credit_card_showed','is_fraud']


#### help fun

## Get Data Functions
def GetCities()->dict:
   conn = create_connection(db_file)
   cur = conn.cursor()
   sql_query = pd.read_sql_query ('''SELECT * FROM frauddetection_cityInData''', conn)
   CityID = {}
   CityIDandLocationTuple = {}
   for index,row in sql_query.iterrows():
      CityID[row['nameOfCity']] = row["id"]
      CityIDandLocationTuple[row["id"]] = (row["Latitude"],row["Longitude"])
   return CityID,CityIDandLocationTuple

def GetData()-> pd.DataFrame():
   conn = create_connection(db_file)
   cur = conn.cursor()
   sql_query = pd.read_sql_query ('''SELECT * FROM frauddetection_data_charge''', conn)
   df = pd.DataFrame(sql_query, columns = cl)
   return df
   
def create_connection(db_file):
   try:
      conn = sqlite3.connect(db_file)
   except sqlite3.Error as e:
      print(e)
      return None

   return conn

## Convert Functions

def TimetoNumber(time) -> int:

   newtime = datetime.datetime.strptime(time , '%H:%M:%S')
   h = newtime.hour
   m = newtime.minute
   time_num = h*100 + m
   return time_num
   

def makeDatecoltoDayMonthYearCols(DateCol):
   dayList = []
   monthList = []
   yearList = []
   
   for index, row in DateCol.items():
      
      newdate = datetime.datetime.strptime(row , '%Y-%m-%d').date()
      dayList.append(newdate.day)
      monthList.append(newdate.month)
      yearList.append(newdate.year)
   return dayList,monthList,yearList

def MakeDistaneCol(df:pd.DataFrame,CitiesLocations:dict)->list:
   distanceList = []
   for index,row in df.iterrows():
      location1 = CitiesLocations[row[cl[2]]]
      location2 = CitiesLocations[row[cl[8]]]
      distanceList.append(GetDistance(location1,location2))
   return distanceList


def GetDistance(location1:tuple,locatin2:tuple) -> float: ## location is (Latitude,Longitude)
   return geoD.distance(location1,locatin2).km

def MakeDayinWeekCol(DateCol):
   dayinweekList = []
   for index,row in DateCol.items():
      newdate = datetime.datetime.strptime(row , '%Y-%m-%d').date()
      dayinweekList.append(datetime.datetime.isoweekday(newdate))
   return dayinweekList




## Prepare DF 

def PrepareDF(df):
  
   
   ## split to x and y
   X = df.drop([cl[10]] ,axis=1)
   Y = df[cl[10]]

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
   CityinData,CityIDandLocationTuple= GetCities()
   
   
   new_x = X.copy()
   new_x.replace({cl[3]:dictGender,cl[6]:dictTime,cl[8]:CityinData,cl[2]:CityinData},inplace=True)
   new_x["distaneKm"] = MakeDistaneCol(new_x,CityIDandLocationTuple)
   new_x["dayInWeek"] = MakeDayinWeekCol(new_x[cl[7]])
   new_x[cl[5]] = new_x[cl[5]].apply(TimetoNumber)
   dayList,monthList,yearList = makeDatecoltoDayMonthYearCols(new_x[cl[7]])
   new_x = new_x.drop([cl[7]] ,axis=1)
   new_x['day_of_debit'] = dayList
   new_x['month_of_debit'] = monthList
   new_x['year_of_debit'] = yearList
   
   

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
      
## Train DF
def Train(Tdata : pd.DataFrame):## params = panada.df goal = to train model 
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


#will be in the server side need to be deleted
def Prediction(KNearest_model,DecisionTreeClassifier_model,data):## input 2 models and data to predict -> uotput us a list of the rows that could be fraud
    
    if KNearest_model is None or DecisionTreeClassifier_model is None:
      return []
    
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
   df =  GetData()
   Train(df)
   
   
   

  
    
if __name__ == "__main__":
    main()







