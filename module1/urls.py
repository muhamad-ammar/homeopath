from os import name
from django.contrib import admin
from django.urls import path
from .views import login_view, logout_view,Home_View, register_view,search_view,table_view
urlpatterns = [

    path('login/', login_view,name="login"),
    path('', login_view,name="login"),
    path('logout/', logout_view,name="logout"),
    path('register/', register_view,name="register"),
    path('home', Home_View,name="home"),
    path('search_view',search_view,name='search_view'),
    path('table_view',table_view,name='table_view'),
    # path('tab_remedy/<keyword>', remedy_view, name='tab_remedy'),
    #path('tab_remed',remedy_view,name="tab_remedy")
    
]