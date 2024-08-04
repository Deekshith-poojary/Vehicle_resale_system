from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import car_details, user_details 
        
def signin(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
      return HttpResponse("Invalid credentials.<a href='/'>Home</a>")
    login(request, user)
    return redirect('/cars/')
  else:
    return render(request, 'login.html')
			
def signout(request):
	logout(request)
	return redirect('/')
	
def signup(request):
  if request.method=="POST":
    username = request.POST['username']
    password = request.POST['password']
    phone = request.POST['phone']
    email = request.POST['email']
    newuser = User.objects.create_user(
			username=username,
			password=password,
			email=email
		)
    user_detail=user_details(user_name=username,phone=phone,email=email)
    try:
      newuser.save()
      user_detail.save()
      return render(request, 'signup.html')  
    except:
      return HttpResponse("Something went wrong.")
  else:
    return render(request, 'signup.html')  

# Create your views here.

def cars_list(request):
    if request.user.is_authenticated:
      name=car_details.objects.raw('select * from cars_car_details')
      dict={'name':name}
      return render(request,'cars.html',dict)
    else:
      return redirect('/cars/login/')

def car_info(request,car_id):
    if request.user.is_authenticated:
      car_detail=car_details.objects.raw('select * from cars_car_details where car_id = "'+str(car_id)+'"')
      name=car_detail[0].username
      query='select * from cars_user_details where user_name = "'+name+'"'
      user_detail=user_details.objects.raw(query)
      dict={'car':car_detail,'user':user_detail[0]}
      return render(request,'car_details.html',dict)
    else:
      return redirect('/cars/login/')

def search(request):
    lis=request.GET.get('as')
    return render(request,'search.html')

def sell(request):
    if request.method=="POST":
      car_name = request.POST['car_name']
      car_type = request.POST['car_type']
      make = request.POST['make']
      model = request.POST['model']
      first_registration = request.POST['first_registration']
      Milage = request.POST['Milage']
      fuel = request.POST['fuel']
      eng_size = request.POST['eng_size']
      power = request.POST['power']
      Gearbox = request.POST['Gearbox']
      seats = request.POST['seats']
      color = request.POST['color']
      price = request.POST['price']
      description = request.POST['description']
      image = request.FILES['image']
      print(image)
      n=car_details(car_name=car_name,car_type=car_type,car_make=make,car_model=model,first_reg=first_registration,milage=Milage,fuel=fuel,eng_size=eng_size,power=power,gear_box=Gearbox,seats=seats,color=color,price=price,desciption=description,image=image,username=request.user)
      n.save()
    if request.user.is_authenticated:
      return render(request,'sell.html')
    else:
      return redirect('/cars/login/')

      