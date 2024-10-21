from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import *
from .forms import * 
from django.views.generic import UpdateView
from .models import Profile
from .forms import UpdateProfileForm
from django.urls import reverse

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
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        # Save the status message to the database
        sm = form.save()

        # Handle file uploads (images)
        files = self.request.FILES.getlist('files')
        print(f"Uploaded files: {files}")  # Check if files are being uploaded
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()
            print(f"Saved image: {image.image_file.url}")  # Check the image URL after saving

        return super().form_valid(form)


    def get_success_url(self):
        # Redirect back to the profile page after the status message is created
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        # Add the profile object to the context
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        # Redirect to the profile page after the profile is updated
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect back to the profile page after deleting the status message
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect back to the profile page after updating the status message
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})