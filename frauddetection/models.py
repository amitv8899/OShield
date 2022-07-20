from django.db import models


# Create your models here.
class CityInData(models.Model):
    nameOfCity = models.CharField(max_length=30)

class Data_charge(models.Model):
    usr_id = models.IntegerField(verbose_name="id_Username",null = False,default=0)
    age = models.IntegerField(verbose_name="age",null= False)
    cityLiveIn = models.IntegerField(verbose_name="city live in",null= False)
    gender = models.CharField(verbose_name="gender",max_length=1,null= False)
    amount = models.IntegerField(verbose_name="amount",null=False)
    hour_of_debit = models.TimeField(verbose_name="hour_of_debit",null = False)
    time_of_debit = models.IntegerField(verbose_name="time_of_debit",null= False)
    day_of_debit = models.IntegerField(verbose_name="day_of_debit",null=False)
    month_of_debit = models.IntegerField(verbose_name="month_of_debit",null=False)
    year_of_debit = models.IntegerField(verbose_name="year_of_debit",null=False)
    day_of_debit = models.IntegerField(verbose_name="day_of_debit",null=False)
    city_of_debit = models.IntegerField(verbose_name="city_of_debit",null= False)
    credit_card_showed = models.BinaryField(verbose_name="credit_card_showed",null= False)
    is_fraud = models.BinaryField(verbose_name="is_fraud",null = False)

    

    



