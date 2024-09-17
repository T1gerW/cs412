## hw/urls.py
## description: URL patterns for the hw app 

from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 

# all of the URLS that are part of this app 
urlpatterns = [
    path(r'', views.home, name = "home"),
]