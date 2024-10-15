from django.db import models

# Create your models here.
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(blank=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        # This will reverse the 'show_profile' URL and pass the profile's primary key (pk)
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically set the current timestamp
    message = models.TextField()  # Text of the status message
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)  # Relationship to the Profile model

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp}: {self.message[:20]}..."  # Shows first 20 chars of message
    

