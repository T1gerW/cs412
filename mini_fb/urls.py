#mini_fb/urls.py
## description: URL patterns for the mini_fb app 

from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 
from django.conf.urls.static import static

# all of the URLS that are part of this app 
urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name = "show_all"),
    ##path(r'about', view.home, name = "about")

] + static(settings.STATIC_URL,
           document_root = settings.STATIC_ROOT)
