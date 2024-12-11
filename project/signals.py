from django.db.models.signals import post_save  # Signal triggered after a model's save() method is called
from django.dispatch import receiver  # Decorator to define a function as a signal receiver
from django.contrib.auth.models import User  # Built-in User model for authentication
from .models import Member  # Custom Member model associated with User

# Signal to automatically create a Member instance whenever a new User is created
@receiver(post_save, sender=User)  # Connect this function to the post_save signal of the User model
def create_member_for_user(sender, instance, created, **kwargs):
    """
    Signal to create a Member profile for a newly created User.
    Triggered automatically after a User instance is saved.
    
    Args:
        sender: The model class that sent the signal (User in this case).
        instance: The instance of the model being saved.
        created: Boolean indicating whether a new instance was created.
        kwargs: Additional keyword arguments.
    """
    if created:  # Only execute this logic if a new User instance was created
        Member.objects.create(
            user=instance,  # Associate the Member with the newly created User
            first_name=instance.first_name,  # Copy the first name from the User
            last_name=instance.last_name,  # Copy the last name from the User
            email=instance.email  # Copy the email from the User
        )
