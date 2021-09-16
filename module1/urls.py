from os import name
from django.contrib import admin
from django.urls import path,re_path
from .views import feedback_view, login_view, logout_view,Home_View, register_view,search_view,table_view,submit_view
urlpatterns = [

    path('login/', login_view,name="login"),
    path('logout/', logout_view,name="logout"),
    path('register/', register_view,name="register"),
    path('home', Home_View,name="home"),
    path('search_view',search_view,name='search_view'),

    path('submit_view',submit_view,name='submit_view'),
    path('feedback',feedback_view,name='feedback_view'),

    re_path(r'^ajax/get_response/$', table_view, name='get_response')
    ('', table_view, name='get_response')
    # path('tab_remedy/<keyword>', remedy_view, name='tab_remedy'),
    #path('tab_remed',remedy_view,name="tab_remedy")
    
]
