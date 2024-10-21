from django import forms
from .models import Profile
from .models import StatusMessage

# CreateProfileForm which inherits from ModelForm
class CreateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile  # Specify the model this form is related to
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']  # Specify all fields of the Profile model


class CreateStatusMessageForm(forms.ModelForm):
    
    class Meta:
        model = StatusMessage  # Specify the model for the form
        fields = ['message']  # Only the 'message' field is required from the user

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']  # Exclude first_name and last_name
