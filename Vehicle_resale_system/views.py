from django.shortcuts import render
from cars.models import car_details, user_details 

def index(request):
    name=car_details.objects.raw('select * from cars_car_details where car_id between 1 and 3')
    dict={'name':name,'range':[1,2,3]}
    return render(request,'index.html',dict)

