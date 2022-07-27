from distutils.command.clean import clean
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class RegisterForm(UserCreationForm):
	
    birth = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    cityLiveIn = forms.CharField(required=True)
    gender = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ("username","email","birth","cityLiveIn","gender","password1","password2")

    def save(self,commit = True):
        user = super(RegisterForm,self).save(commit = False)
        user.set_age()
        if commit:
          user.save()
        return user

class MainUserForm(forms.Form):
  pass

  