from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('<int:year>/<int:month>/<int:date>/', views.date),
]
