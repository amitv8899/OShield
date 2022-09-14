from django.db import models


# Create your models here.
class CityInData(models.Model):
    nameOfCity = models.CharField(max_length=30)
    Latitude = models.FloatField(default=0)
    Longitude = models.FloatField(default=0)

    def __str__(self):
        return self.nameOfCity


class Data_charge(models.Model):
    
    user_id = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    cityLiveIn = models.IntegerField(null=True)
    gender = models.CharField(max_length = 1,null=True)
    amount = models.IntegerField(null=True)
    hour_of_debit = models.TimeField(null=True)
    time_of_debit = models.CharField(max_length = 2,null=True)
    date_of_debit = models.DateField(null=True)
    city_of_debit = models.IntegerField(null=True)
    credit_card_showed = models.IntegerField(null=True)
    is_fraud = models.IntegerField(null=True)
    
    


    

    



