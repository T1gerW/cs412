## hw/urls.py
## description: URL patterns for the hw app 

from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 
from django.conf.urls.static import static

# all of the URLS that are part of this app 
urlpatterns = [
    path(r'', views.home, name = "home"),

] + static(settings.STATIC_URL,
           document_root = settings.STATIC_ROOT)