from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)  # Replace 1 with the ID of your admin user
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
    
    def get_friends(self):
        # Query for friends where this profile is either profile1 or profile2
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        # Collect all friend profiles
        friends = []
        for friend in friends_as_profile1:
            friends.append(friend.profile2)  # The other friend is in profile2
        for friend in friends_as_profile2:
            friends.append(friend.profile1)  # The other friend is in profile1

        return friends
    
    def add_friend(self, other):
        # Prevent self-friending
        if self == other:
            return "Cannot friend yourself."

        # Check if a friendship already exists (in either order)
        existing_friendship = Friend.objects.filter(
            Q(profile1=self, profile2=other) | Q(profile1=other, profile2=self)
        ).exists()

        if existing_friendship:
            return "Friendship already exists."

        # Create the new friendship
        new_friendship = Friend(profile1=self, profile2=other)
        new_friendship.save()
        return "Friendship created successfully."
    
    def get_friend_suggestions(self):
        # Step 1: Find profiles that are already friends with the current profile
        # Get all friends where this profile is either profile1 or profile2
        friends = Friend.objects.filter(
            Q(profile1=self) | Q(profile2=self)
        )

        # Extract the actual friend profiles from the Friend relationships
        friend_ids = set()
        for friend in friends:
            if friend.profile1 == self:
                friend_ids.add(friend.profile2.id)
            else:
                friend_ids.add(friend.profile1.id)

        # Step 2: Exclude current friends and the profile itself from suggestions
        suggestions = Profile.objects.exclude(id__in=friend_ids).exclude(id=self.id)

        # Optional: Limit the number of suggestions
        return suggestions
    
    def get_news_feed(self):
        # Step 1: Get all friend profiles using the existing get_friends method
        friends = self.get_friends()

        # Step 2: Collect IDs of this profile and its friends
        profile_ids = [friend.id for friend in friends]
        profile_ids.append(self.id)

        # Step 3: Retrieve all StatusMessages for this profile and friends, ordered by timestamp
        news_feed = StatusMessage.objects.filter(profile__id__in=profile_ids).order_by('-timestamp')

        return news_feed


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)  # Automatically set the current timestamp
    message = models.TextField()  # Text of the status message
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)  # Relationship to the Profile model

    def __str__(self):
        return f"Status by {self.profile.first_name} on {self.timestamp}: {self.message[:20]}..."  # Shows first 20 chars of message
    
    def get_images(self):
        # Retrieve all images associated with this StatusMessage
        return self.images.all()  # `images` is the related_name from the Image model

class Image(models.Model):
    # The image file field that will store the image in the media directory
    image_file = models.ImageField(upload_to='status_images/')  # Stores images in media/status_images/
    
    # Timestamp of when the image was uploaded
    timestamp = models.DateTimeField(default=timezone.now)
    
    # ForeignKey to the StatusMessage model (many-to-one relationship)
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for StatusMessage {self.status_message.id} uploaded on {self.timestamp}"

class Friend(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)

    #  Foreign keys to the Profile model, representing two friends
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1_friends")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2_friends")

     # String representation of the friendship
    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
    


    

