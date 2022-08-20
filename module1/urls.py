from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LogoutView
from .views import feedback_view, login_view, logout_view,Home_View, register_view,search_view,table_view,submit_view,repo_view,saveFeedbackForm,patientFeedbackForm,feedback_filter_view,case_analysis,getRating

urlpatterns = [

    path('login/', login_view,name="login"),
    path('logout/', logout_view,name="logout"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', register_view,name="register"),
    path('', Home_View,name="home"),
    path('home', Home_View,name="home"),
    path('search_view',search_view,name='search_view'),
    path('search',table_view,name='search'),
    path('repo',repo_view,name='repo'),
    path('submit_view',submit_view,name='submit_view'),
    path('feedback',feedback_view,name='feedback_view'),
    path('feedback_filter_view',feedback_filter_view,name='feedback_filter_view'),
    path('case_analysis',case_analysis,name='case_analysis'),
    path('getRating',getRating,name='getRating'),
    path('saveFeedbackForm',saveFeedbackForm,name='saveFeedbackForm'),
    path('patientFeedbackForm',patientFeedbackForm,name='patientFeedbackForm'),

    # re_path(r'^ajax/get_response/$', table_view, name='get_response'),
    # re_path('', table_view, name='get_response')
    # path('tab_remedy/<keyword>', remedy_view, name='tab_remedy'),
    #path('tab_remed',remedy_view,name="tab_remedy")
    
]
