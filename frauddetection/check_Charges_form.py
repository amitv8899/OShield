from distutils.command.clean import clean
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class upload_charges(forms.form):
    chargeCreditCompany = forms.ChoiceField(choices=['leumi' ,'Cal'])
    file=forms.FileField()

