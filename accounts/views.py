from ast import Return
from urllib import response
from wsgiref.util import request_uri
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login,authenticate 
from django.contrib.auth.forms import UserCreationForm
from .form import RegisterForm , MainUserForm
# Create your views here.

def home(response):
    return render(response,"accounts/base.html",{})

def Register(request):

    if request.method == "POST":
       print(request.POST)
        
       
       form = RegisterForm(request.POST)
       if form.is_valid():
           form.save()
           username = request.POST['username']
           password = request.POST['password1']
           
           user = authenticate(request, username=username, password=password)
          
           if user is not None:
              login(request, user)
              context = {"Cusername":username}
              return render(request,"accounts/UserHome.html",context)
           else:
              context = {"Msg_to_user":"problem in register prosess please register agai"}
              return render(request,"OSheild/generic.html",context)
                    
    else:
        form = RegisterForm()
        
    return render(request,"accounts/register.html",{"form":form})

def LogIn(request):

    if request.user.is_authenticated:
      context = {"Msg_to_user":"already login"}
      return render(request,"OSheild/generic.html",context)
    print("hello")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


def UserHome(request):
    
    if not request.user.is_authenticated:
      context = {"Msg_to_user":"To get the service please login "}
      return render(request,"OSheild/generic.html",context)
    
    currentUser = request.user
    username = currentUser.__str__
    context = {"Cusername":username}

    return render(request,"accounts/UserHome.html",context)      

            
    

  