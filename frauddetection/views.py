from django.shortcuts import render
from argparse import FileType
from msilib.schema import File
from telnetlib import STATUS
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd

# Create your views here.

def check_form_view(request):

         if request.method == "POST":
            upload_file = request.FILES['charge']
            df = pd.read_excel(upload_file)
            print(request.user)
    

            return HttpResponse("ok")
          
         else:
            return render(request,"frauddetection/check_charges.html")




