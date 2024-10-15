from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import * 


# class-based view 
class ShowAllView(ListView):
    '''the view to show all Profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' #context variable used in template

class ShowProfilePageView(DetailView):
    '''the view to show a single profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    model = Profile  # Specify the model this view is associated with
    form_class = CreateProfileForm  # Use the CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'  # Template to render the form

    # Optionally, you can define a success URL to redirect to after a profile is successfully created
    success_url = '/mini_fb/'  # Redirect to the profile list page (or another page) after successful creation

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        # Assign the profile to the status message before saving
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the profile page after the status message is created
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        # Step (a): Look up the Profile object using the pk in self.kwargs
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Step (b): Attach the Profile object to the status message
        form.instance.profile = profile
        
        # Save the form and create the StatusMessage
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Add the profile object to the context
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile  # Add profile to context
        return context