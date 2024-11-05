from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, DeleteView,View
from .models import *
from .forms import * 
from django.views.generic import UpdateView
from .models import Profile
from .forms import UpdateProfileForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

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

    def get_object(self, queryset=None):
        # Check if a primary key (pk) is present in the URL
        pk = self.kwargs.get('pk')
        if pk:
            # Attempt to fetch the profile based on the provided pk
            try:
                return Profile.objects.get(pk=pk)
            except Profile.DoesNotExist:
                raise Http404("Profile does not exist")
        else:
            # If no pk is provided, show the profile for the logged-in user
            return Profile.objects.get(user=self.request.user)

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'mini_fb/create_profile_form.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('show_all_profiles')  # Redirect to a page after successful creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add UserCreationForm to the context
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Reconstruct the UserCreationForm with POST data to validate and save it
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the new User instance
            user = user_form.save()
            # Attach the newly created user to the profile
            form.instance.user = user
            # Save the Profile instance with the user attached
            return super().form_valid(form)
        else:
            # If UserCreationForm is not valid, re-render the page with errors
            return self.form_invalid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    template_name = 'mini_fb/create_status_form.html'
    fields = ['message']

    def form_valid(self, form):
        # Attach the logged-in user's profile to the new status message
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile page after creating a status
        return reverse_lazy('show_profile')

    def get_context_data(self, **kwargs):
        # Provide the profile of the logged-in user to the template context, not pk
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_object(self, queryset=None):
        # Find the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'mini_fb/update_profile_form.html'
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']

    def get_success_url(self):
        # Redirect to the profile page after the profile is updated
        print("Redirecting to show_profile") 
        return reverse_lazy('show_profile')
    
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        # Find the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not form.is_valid():
            print("Form validation failed:", form.errors)  # Debugging statement
        return form
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect to the profile page of the profile associated with the status message
        profile_id = self.object.profile.pk
        return reverse('view_profile', kwargs={'pk': profile_id})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        # Redirect back to the specific profile page associated with the updated status message
        return reverse('view_profile', kwargs={'pk': self.object.profile.pk})
    
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile')
    

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get friend suggestions for the profile
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        
        return context
    
    def get_object(self, queryset=None):
        # Find the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the news feed for the profile
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        
        return context
    
    def get_object(self, queryset=None):
        # Find the profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)
    
class CustomLoginView(auth_views.LoginView):
    template_name = 'mini_fb/login.html'  # Specify the custom template

    def get_login_url(self):
        return reverse('login')  # Custom login URL