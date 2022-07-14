#
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

fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier.sav'
fileLogisticRegression_model = 'LogisticRegression.sav'

def GetData(request):
    if request.method == "GET":
        if request.GET["password"] == "model123456789":
            df =  pd.DataFrame(list(Data_charge.objects.all().values()))
            print(df)
            dataPickled = pickle.dumps(df)
            data_b64 =  base64.b64encode(dataPickled)
            print(data_b64)
            DatatoSend = data_b64.decode('utf-8')
            print(DatatoSend)
        
            return  HttpResponse(DatatoSend, status=200)
        else:
            return HttpResponse('Unauthorized1', status=401)
    return HttpResponse('Unauthorized2', status=401)

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
    
  

