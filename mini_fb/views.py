from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *


# class-based view 
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' #context variable used in template