#blog/views.py
# define views for blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *


# class-based view 
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context variable used in template
    


