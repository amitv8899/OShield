from django.db import models


# Create your models here.
class CityInData(models.Model):
    nameOfCity = models.CharField(max_length=30)

class Data_charge(models.Model):
    usr_id = models.IntegerField(verbose_name="id_Username",null = True,default=0)
    age = models.IntegerField(verbose_name="age",null= True,default=None)
    cityLiveIn = models.CharField(verbose_name="city live in",max_length=30,null= True,default=None)
    gender = models.CharField(verbose_name="gender",max_length=1,null= True,default=None)
    amount = models.IntegerField(verbose_name="amount",null=True,default=None)
    hour_of_debit = models.TimeField(verbose_name="hour_of_debit",null = True,default=None)
    time_of_debit = models.IntegerField(verbose_name="time_of_debit",null= True,default=None)
    city_of_debit = models.CharField(verbose_name="city_of_debit",max_length=30,null= True,default=None)
    credit_card_showed = models.BinaryField(verbose_name="credit_card_showed",null= True,default=None)
    is_fraud = models.BinaryField(verbose_name="is_fraud",null = True,default=None)

    

    



