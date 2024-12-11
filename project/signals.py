from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member

@receiver(post_save, sender=User)
def create_member_for_user(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )
