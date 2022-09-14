#general
import numpy as np
import pandas as pd
import datetime
import geopy.distance as geoD

#fix data
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split

#models
import sqlite3
import pickle
from pathlib import Path

## django 
from .models import CityInData,Data_charge
from django.http import HttpResponse


#static
fileKNearest_model = 'KNearest_model.sav'
fileDecisionTreeClassifier_model = 'DecisionTreeClassifier_model.sav'
fileLogisticRegression_model = 'LogisticRegression_model.sav'

cl = ['user_id', 'age', 'cityLiveIn','gender','amount',
   'hour_of_debit','time_of_debit','date_of_debit','city_of_debit','credit_card_showed','is_fraud']

def GetDicOfCityInData() -> dict:
   all =  CityInData.objects.all()
   CityDict = {}
   CityIDandLocationTuple = {}
   for city in all:
      CityDict[city.nameOfCity] = city.id
      CityIDandLocationTuple[city.id] = (city.Latitude,city.Longitude)
   return CityDict,CityIDandLocationTuple

def create_connection(db_file):
   try:
      conn = sqlite3.connect(db_file)
   except sqlite3.Error as e:
      print(e)
      return None

   return conn

def makeDatecoltoDayMonthYearCols(DateCol:pd.DataFrame()):
   dayList = []
   monthList = []
   yearList = []
   
   for index, row in DateCol.items():
      dayList.append(row.day)
      monthList.append(row.month)
      yearList.append(row.year)
   return dayList,monthList,yearList

def TimetoNumber(time: datetime.time) -> int:
   h =time.hour
   m = time.minute
   time_num = h*100 + m

   return time_num

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
      dayinweekList.append(datetime.datetime.isoweekday(row))
   return dayinweekList



def PrepareDF(df :pd.DataFrame()):
   
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
   CityinData,CityIDandLocationTuple = GetDicOfCityInData()

   
   df.replace({cl[3]:dictGender,cl[6]:dictTime,cl[8]:CityinData,cl[2]:CityinData},inplace=True)
   df["DistaneKm"] = MakeDistaneCol(df,CityIDandLocationTuple)
   df["dayInWeek"] = MakeDayinWeekCol(df[cl[7]])
   df[cl[5]] = df[cl[5]].apply(TimetoNumber)
   dayList,monthList,yearList = makeDatecoltoDayMonthYearCols(df[cl[7]])
   df =df.drop([cl[7]] ,axis=1)
   df['day_of_debit'] = dayList
   df['month_of_debit'] = monthList
   df['year_of_debit'] = yearList
   
   return df

def Prediction(data : pd.DataFrame) -> list[int]:## input 2 models and data to predict -> uotput us a list of the rows that could be fraud
   
    ReadyData= PrepareDF(data)
    
    KNearest_model,DecisionTreeClassifier_model = LoadModels()
    if KNearest_model is None or DecisionTreeClassifier_model is None:
      return None

    KNearest_model_P = KNearest_model.predict(ReadyData.to_numpy())
    
    DecisionTreeClassifier_model_P = DecisionTreeClassifier_model.predict(ReadyData.to_numpy())
    
    fruad = [l1+l2 for l1,l2 in zip(DecisionTreeClassifier_model_P,KNearest_model_P)]
    return [i for i,val  in enumerate(fruad) if val > 1]
   
def LoadModels():

    dirPath = str(Path(__file__).parents[1])
    

    try:
       KNearest_model = pickle.load(open(dirPath+"\\"+fileKNearest_model, 'rb'))
       
       DecisionTreeClassifier_model = pickle.load(open(dirPath+"\\"+fileDecisionTreeClassifier_model, 'rb'))
       ##LogisticRegression_model = pickle.load(open(dirPath+"\\"+fileLogisticRegression_model, 'rb'))
    except OSError as err:
       print("OS error: {0}".format(err))
       return None,None
    return KNearest_model,DecisionTreeClassifier_model

def AppendUserToDF(user,chargeToPredict):
   
   user_id =  user.id
   age = user.age
   cityLiveIn = user.cityLiveIn
   gender = user.gender
   UserWithdata = pd.DataFrame(columns=cl)

   for index,row in chargeToPredict.iterrows():#create new dataframe to send to predict
      try:
        date = datetime.date(row["date_of_debit"].year,row["date_of_debit"].month, row["date_of_debit"].day)
      except:
         date = datetime.date(2000,12,12)#defult year

      if VaildData(user_id,age,cityLiveIn,gender,row["amount"],row["hour_of_debit"],row["time_of_debit"],date,row["city_of_debit"],row["credit_card_showed"],0):
       new_row = {
       cl[0]:user_id,
       cl[1]:age,
       cl[2]:cityLiveIn,
       cl[3]:gender,
       cl[4]:row["amount"],
       cl[5]:row["hour_of_debit"],
       cl[6]:row["time_of_debit"],
       cl[7]:date,
       cl[8]:row["city_of_debit"],
       cl[9]:row["credit_card_showed"],
       cl[10]:0}
       UserWithdata = UserWithdata.append(new_row, ignore_index = True)
       
      #else:
      #    do not include in data

   return UserWithdata

    
def FraudResuilt(user,chargeToPredict):
   
   new_data = AppendUserToDF(user,chargeToPredict)
   
   tempData = new_data.drop([cl[10]] ,axis=1)

   AllFruad = Prediction(tempData)
   

   return new_data,AllFruad
   
   
def SaveData(df :pd.DataFrame,IsTrainData):# not neeed to check vailtions because its our data 

   for index,row in df.iterrows():
      id_user = row[cl[0]]
      age = row[cl[1]]
      cityLiveIn = row[cl[2]]
      gender = row[cl[3]]
      amount = row[cl[4]]
      hour = row[cl[5]]
      time = row[cl[6]]
      date = datetime.date(row[cl[7]].year, row[cl[7]].month, row[cl[7]].day) if IsTrainData else row[cl[7]] # as exel is save as timestamp
      city = row[cl[8]]
      cardShowed = row[cl[9]]
      fraud = row[cl[10]]

      if CityInData.objects.filter(nameOfCity = cityLiveIn).exists() and CityInData.objects.filter(nameOfCity = city).exists():
         
         cityLiveInID =CityInData.objects.get(nameOfCity = cityLiveIn).id
         city_of_debitID = CityInData.objects.get(nameOfCity = city).id

         Data_charge.objects.create(
         user_id = id_user,
         age = age,
         cityLiveIn= cityLiveInID,
         gender = gender ,
         amount = amount,
         hour_of_debit =hour,
         time_of_debit = time,
         date_of_debit =date,
         city_of_debit = city_of_debitID,
         credit_card_showed =cardShowed,
         is_fraud = fraud)

   return True
         

def VaildData(*data):
   
   if len(data) !=11:
      print("len")
     
      return False

   if type(data[0]) is not int:#user_id
      print(0)
     
      #raise ValueError("error val: {}, index: {}".format(data[1],1))
      return False
   elif type(data[1]) is not int:#ag
      print(1)
      #raise ValueError("error val: {}, index: {}".format(data[1],1))
      return False
   elif type(data[2]) is not str:#cityLiveIn // before id check
      print(2)
      #raise ValueError("error val: {}, index: {}".format(data[2],2))
      return False
   elif type(data[3]) is not str and len(data[3]) == 1 :#gender m/M or f/F
      print(3)
      #raise ValueError("error val: {}, index: {}".format(data[3],3))
      return False
   elif type(data[4]) is not int:#amount
      print(4)
      #raise ValueError("error val: {}, index: {}".format(data[4],4))
      return False
   elif type(data[5]) is not datetime.time:#hour_of_debit
      print(5)
      #raise ValueError("error val: {}, index: {}".format(data[5],5))
      return False
   elif (data[6] !='am' and data[6] !='AM' and data[6] !='pm' and data[6] !='PM'):#time_of_debit + am/AM or pm/PM 
      print(6)
      #raise ValueError("error val: {}, index: {}".format(data[6],6))
      return False
   elif type(data[7]) is not datetime.date:#date_of_debit
      print(7)
      #raise ValueError("error val: {}, index: {}".format(data[7],7))
      return False
   elif type(data[8]) is not str:#city_of_debit
      print(8)
      #raise ValueError("error val: {}, index: {}".format(data[8],8))
      return False
   elif (data[9] != 1 and data[9] != 0):#credit_card_showed
      print(9)
      #raise ValueError("error val: {}, index: {}".format(data[9],9))
      return False
   elif (data[10] != 1 and data[10] != 0):#is_fraud
      print(10)
      #raise ValueError("error val: {}, index: {}".format(data[10],10))
      return False

   return True
   


   


   