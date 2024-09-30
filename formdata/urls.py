from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 

urlpatterns = [
    path(r'', views.show_form, name = "show_form"), ##new app from class
    path(r'submit', views.submit, name = "submit") 
    
]
