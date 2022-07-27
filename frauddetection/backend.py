#
from xmlrpc.client import Boolean
import numpy as np
import pandas as pd
import datetime

from urllib3 import HTTPResponse

#get data
from . import models

#fix data
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
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
## django 
from .models import Data_charge
import base64
from django.http import HttpResponse

import sqlite3
from . import models


fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier.sav'
fileLogisticRegression_model = 'LogisticRegression.sav'

db_file = 'C:\\Users\\AMIT\\workpalce\\django-proj\\db.sqlit3'


def create_connection(db_file):
   try:
      conn = sqlite3.connect(db_file)
   except sqlite3.Error as e:
      print(e)
      return None

   return conn

def IsCityInData(city):
   conn = create_connection(db_file)
   cur = conn.cursor()
   cur.execute('''SELECT nameOfCity FROM frauddetection_CityInData WHERE nameOfCity=?''',(city))
   return cur.fetchone()
   

def PrepareDF(df):
   Y = None
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
    # replace cities to number -> need to make it dict!!!
   dictCities = (models.CityInData.objects.values('id','nameOfCity'))
   

   new_x = X.copy()
   new_x.replace({"gender":dictGender,"time of debit":dictTime,'live city':dictCities,'city of debit':dictCities},inplace=True)
   new_x["hour_of_debit"] = new_x["hour_of_debit"].apply(time_to_number)
        
   return new_x,Y

def time_to_number(time: datetime.time) -> int:
   strh = time.strftime("%H")
   strm = time.strftime("%M")
   time_num = (int(strh)*100) + int(strm)

   return time_num

def Prediction(data : pd.DataFrame) -> list[int]:## input 2 models and data to predict -> uotput us a list of the rows that could be fraud
    X,Y = PrepareDF(data,False)
    KNearest_model,DecisionTreeClassifier_model = LoadModels()

    KNearest_model_P = KNearest_model.predict(X.to_numpy())
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
    

<<<<<<< HEAD

def fraudResults(charges,bank_name,user):
    df_charges = pd.read_excel('charges.xlsx')
    data_user = {'id': [user.id],
                'age': [user.age],
                'live city': [user.cityLiveIn],
                'gender': [user.gender] }
    
    df_user = pd.DataFrame(data_user)
    
    frames = [df_user, df_charges]
    df_total = pd.concat(frames)

    

    # df_total_to amit prediction 

    #after pred i need to add row yo sql

=======
def FraudResuilt(User,chargeToPredict):
  
>>>>>>> amit_work


   pass
   