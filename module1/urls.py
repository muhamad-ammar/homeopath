from os import name
from module1.views import login
from django.contrib import admin
from django.urls import path
from .views  import signup,login
urlpatterns = [
    path('login/',login,name="login" ),
    path('register/',signup,name="signup" ),
]