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
    
  

