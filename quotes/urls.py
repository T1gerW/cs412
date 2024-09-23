from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 
from django.conf.urls.static import static

urlpatterns = [
    path('', views.quote, name='quote'),  # Main page
    path('quote/', views.quote, name='quote'),  # Random quote
    path('show_all/', views.show_all, name='show_all'),  # Show all quotes
    path('about/', views.about, name='about'),  # About page
]

