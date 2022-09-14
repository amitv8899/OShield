from distutils.command.clean import clean
from random import choices
from tkinter import Widget
from unicodedata import name
from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from frauddetection.models import CityInData  
from frauddetection.models import CityInData
from django.core.exceptions import ValidationError
from django import forms

def validate_city(city):
      if not CityInData.objects.filter(nameOfCity = city).exists():
        raise ValidationError(
          ('%(city)s is not in the database!'),
            params={'city': city},
            )
def validate_gender(gender):
  genderOptions = ("M","m","F","f")
  if gender not in genderOptions:    
    raise ValidationError(
      "not vaild gender should be M,m for male and F,f for female")

choicesCities =  CityInData.objects.all().values_list('nameOfCity','nameOfCity')
choices_ListCities =[]
for item in choicesCities:
  choices_ListCities.append(item)
choicesGender = [("M","M"),("F","F")]

class RegisterForm(UserCreationForm):
  
	
    birth = forms.DateField(label ="Full birth",required=True,widget=forms.TextInput(attrs = {"class":"input_field"}))
    email = forms.EmailField(label ="Email",required=True,widget = forms.EmailInput(attrs = {"class":"input_field"}))
    cityLiveIn = forms.CharField(label ="City live in",required=True,validators=[validate_city],widget = forms.Select(choices=choices_ListCities,attrs = {"class":"input_field"}))
    gender = forms.CharField(label ="Gender",required=True,validators=[validate_gender],widget = forms.Select(choices=choicesGender,attrs = {"class":"input_field"}))
    class Meta:
        model = User
        fields = ("username","email","birth","cityLiveIn","gender","password1","password2")
       
    def __init__(self, *args, **kwargs) -> None:
       super(RegisterForm,self).__init__(*args, **kwargs)
       self.fields["username"].widget.attrs["class"] = "input_field"
       self.fields["password1"].widget.attrs["class"] = "input_field"
       self.fields["password2"].widget.attrs["class"] = "input_field"

    def save(self,commit = True):
        user = super(RegisterForm,self).save(commit = False)
        user.set_age()
        if commit:
          user.save()
        return user
    


class MainUserForm(forms.Form):
  pass

  