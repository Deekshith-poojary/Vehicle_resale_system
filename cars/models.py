from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class car_details(models.Model):
    car_id=models.AutoField(primary_key=True)
    car_name=models.CharField(max_length=30)
    car_type=models.CharField(max_length=15)
    car_make=models.CharField(max_length=30)
    car_model=models.CharField(max_length=10)
    first_reg=models.IntegerField()
    milage=models.IntegerField()
    fuel=models.CharField(max_length=10)
    eng_size=models.IntegerField()
    power=models.IntegerField()
    gear_box=models.CharField(max_length=10)
    seats=models.IntegerField()
    color=models.CharField(max_length=10)
    price=models.IntegerField()
    desciption=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='cars',default='')
    username=models.CharField(max_length=20,default='')

class user_details(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=30)
    phone=models.IntegerField()
    email=models.CharField(max_length=50)
