from django.contrib import admin

# Register your models here.

from .models import car_details, user_details
admin.site.register(car_details)
admin.site.register(user_details)