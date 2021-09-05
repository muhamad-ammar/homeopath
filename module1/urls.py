from os import name
from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view,Home_View, register_view
urlpatterns = [

     path('login/', login_view,name="login"),
    path('logout/', logout_view,name="logout"),
    path('register/', register_view,name="register"),
    path('home', Home_View,name="home"),
    
]
