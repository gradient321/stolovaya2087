from django.contrib import admin, staticfiles
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('list/', views.list),
    path('orders/', views.orders),
    path('add/', views.add_order),
    path('chef_order/', views.chef_order),
]