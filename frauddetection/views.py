from datetime import datetime
from difflib import context_diff
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
import pandas as pd
from .backend import FraudResuilt,SaveData,VaildData
from .models import Data_charge,CityInData
from django.urls import reverse
import json
# Create your views here.
def showfrauds(request):
   if not request.user.is_authenticated:
      context = {"Msg_to_user":"To get the service please login "}
      return render(request,"OSheild/generic.html",context)

   old_post = request.session.get('old_post')
   try:
     msgList = old_post["messegeArray"]
     fraudsList = old_post["fraudIndexArray"]
     jsonData = old_post["dataFrameToSave"]
     df = pd.read_json(jsonData, orient ='index')
     
     
     
   except:
      return HttpResponseForbidden("please refres the page and uploade again")
   
   if request.method == "GET":
      msgListAndIndex = tuple(zip(fraudsList, msgList))
      context = {"messegeArray":msgListAndIndex}
      #show user all frauds
      return render(request, "frauddetection/Verifyfrauds.html",context)
     
      
   elif request.method == "POST":
      df['hour_of_debit'] = df['hour_of_debit'].apply(lambda stringtime : datetime.strptime(stringtime,"%H:%M:%S").time()) 
      df['date_of_debit'] = df['date_of_debit'].apply(lambda stringtime : datetime.strptime(stringtime,"%Y-%m-%dT%H:%M:%S.%f%z").date()) 
      arrayOfIndex =  map(int,request.POST.getlist('checks[]'))
      
      for index in arrayOfIndex:
         df.at[index, 'is_fraud'] = 1
      print(df)
      for index,row in df.iterrows():
            
         if not VaildData(row["user_id"],row["age"],row["cityLiveIn"],row["gender"],row["amount"],row["hour_of_debit"],row["time_of_debit"],row["date_of_debit"],row["city_of_debit"],row["credit_card_showed"],row["is_fraud"]):
            return HttpResponse("one val is wrong!")

      
      SaveData(df,False)
      #get from user his fraud 
      currentUser = request.user
      username = currentUser.__str__
      context = {"Cusername":username}
      return render(request,"accounts/UserHome.html",context)
      

   context = {"Msg_to_user":"not vaild http request"}
   return render(request,"OSheild/generic.html",context)

def DateToStr(date:datetime.date)->str:
   day = str(date.day)
   month = str(date.month)
   year = str(date.year)
   return day + "/"+ month + "/" + year

def TimeToStr(time:datetime.time)->str:
   hour = str(time.hour)
   min = str(time.minute)
   return hour + ":" + min

   
def MakeMsg(count, allFraud,df): 
   
   listMesseges =[]
  
   for fraudIndex in allFraud:
      msg = " on the {} at {} a charge of a {} NIS was made in {}".format(df.iloc[fraudIndex]['date_of_debit'],df.iloc[fraudIndex]['hour_of_debit'],df.iloc[fraudIndex]['amount'],df.iloc[fraudIndex]['city_of_debit'])
      listMesseges.append(msg)
   return listMesseges

def check_form_view(request):

   if not request.user.is_authenticated:
      context = {"Msg_to_user":"To get the service please login "}
      return render(request,"OSheild/generic.html",context)
      

   if request.method == "POST":
      upload_file = request.FILES['charge']
      chargeDataFrame = pd.read_excel(upload_file)
      df,allFraud = FraudResuilt(request.user,chargeDataFrame)
      
      if allFraud is None:
        context = {"Msg_to_user":"There is a problem please login later"}
        return render(request,"OSheild/generic.html",context)
      if allFraud == []:
         context = {"Msg_to_user":"We could not find and frauds, your are safe"}
         return render(request,"OSheild/generic.html",context)
      else:#enter to a function
         amountOfFraud = len(allFraud)
         countStr = str(amountOfFraud)
         listMesseges = MakeMsg(amountOfFraud, allFraud,df)#"The system found " + countStr + " Frauds. Please confirm which of the suspected charges are fraudulent",
         jsonDataFrame = df.to_json(orient="index",date_format='iso')
         data  = {"messegeArray":listMesseges, "fraudIndexArray":allFraud,"dataFrameToSave" :jsonDataFrame}
         request.session['old_post'] = data
         return redirect(to='showfrauds')
   else:
      return render(request, "frauddetection/check_charges.html")




def GetTrainData(request):
   if not request.user.is_authenticated:
      context = {"Msg_to_user":"To get the service please login "}
      return render(request,"OSheild/generic.html",context)

   if request.method == "GET":
      return render(request, "frauddetection/check_charges.html")
   if request.method == "POST":
      
      upload_file = request.FILES['charge']
      df = pd.read_excel(upload_file)
      SaveData(df,True)
      return HttpResponse("ok")
      






