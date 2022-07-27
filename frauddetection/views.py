from django.shortcuts import redirect, render
from django.http import HttpResponse

import pandas as pd
from .backend import FraudResuilt

# Create your views here.
def check_form_view(request):

         if request.method == "POST":
            upload_file = request.FILES['charge']
            df = pd.read_excel(upload_file)
            allFraud = FraudResuilt(request.user,df)
            
            return HttpResponse("ok")
          
         else:
            return render(request,"frauddetection/check_charges.html")




