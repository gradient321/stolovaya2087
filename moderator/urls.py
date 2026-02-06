from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('dish/', views.dish),
    path('menu/', views.menu),
    path('orders/', views.orders),
    path('chef_order/', views.chef_order),
    path('chef_order_confirm/<int:id>/', views.chef_order_confirm),
    path('chef_order_cancel/<int:id>/', views.chef_order_cancel),
    path('add/<str:table>/', views.add),
    path('change/<str:table>/<int:id>/', views.change),
    path('delete/<str:table>/<int:id>/', views.delete),
    path('filter/<str:table>/<str:row>/<str:name>/', views.filtered_by),
    path('menu/get_by_date/<int:year>/<int:month>/', views.get_manu_by_date),
    path('menu/get_by_date/<int:year>/<int:month>/<int:day>/', views.get_manu_by_date),
    path('<str:table>/<str:order_by>/', views.order_by),
]