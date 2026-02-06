from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.profile),
    path('pay/', views.pay),
    path('review/', views.review),
    path('subscribe/', views.subscribe),
    path('logout/', views.logout_view)

]
