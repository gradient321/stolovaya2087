from django.contrib import admin
from .models import *

admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Price)
admin.site.register(ChefOrder)