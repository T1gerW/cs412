from django.contrib import admin
from .models import Profile

# Register your models here.


# Register the Profile model to appear in the admin site
admin.site.register(Profile)