from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

# Create your models here.

# Model for Membership Types
class MembershipType(models.Model):
    name = models.CharField(max_length=100)  # Name of the membership type, e.g., Monthly or Yearly
    duration = models.PositiveIntegerField(help_text="Duration in months")  # Duration of the membership in months
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Cost of the membership
    description = models.TextField(blank=True, null=True)  # Optional description for the membership type

    def __str__(self):
        # Return a readable string representation of the membership type
        return f"{self.name} ({self.duration} months - ${self.price})"

# Model for Member
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Associate member with a user
    first_name = models.CharField(max_length=100)  # First name of the member
    last_name = models.CharField(max_length=100)  # Last name of the member
    email = models.EmailField(unique=True)  # Email address, must be unique
    phone_number = models.CharField(max_length=15, default="None")  # Phone number of the member
    membership_type = models.ForeignKey('MembershipType', on_delete=models.SET_NULL, null=True, blank=True)  # Membership type
    join_date = models.DateField(auto_now_add=True)  # Date the member joined, auto-set on creation
    expiration_date = models.DateField(null=True, blank=True)  # Date the membership expires

    def __str__(self):
        # Return a readable string representation of the member
        return f"{self.first_name} {self.last_name} ({self.email})"

    def calculate_expiration_date(self):
        """
        Calculate the expiration date based on the membership type's duration.
        Returns the calculated expiration date or None if no membership type is set.
        """
        if self.membership_type:
            return date.today() + relativedelta(months=self.membership_type.duration)
        return None

    def last_payment_date(self):
        """
        Get the latest payment date for the member.
        Returns the latest payment date or a message indicating no payments have been made.
        """
        latest_payment = Payment.objects.filter(member=self).aggregate(latest=Max('payment_date'))['latest']
        return latest_payment if latest_payment else "No payments made"

# Signal to automatically set the expiration date before saving a member
@receiver(pre_save, sender=Member)
def set_expiration_date(sender, instance, **kwargs):
    """
    Signal to set the expiration date for a member before saving.
    If the expiration date is not already set, calculate it based on the membership type.
    """
    if not instance.expiration_date:
        instance.expiration_date = instance.calculate_expiration_date()

# Model for Member Check-Ins
class CheckIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='checkins')  # Link check-in to a member
    check_in_date = models.DateTimeField(auto_now_add=True)  # Automatically set the check-in date and time

    def __str__(self):
        # Return a readable string representation of the check-in
        return f"Check-In: {self.member} on {self.check_in_date}"

# Model for Payments
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),  # Payment via credit card
        ('cash', 'Cash'),  # Payment via cash
        ('bank_transfer', 'Bank Transfer'),  # Payment via bank transfer
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # Associate payment with a member
    payment_date = models.DateField(auto_now_add=True)  # Automatically set when the payment is made
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount of the payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='credit_card')  # Payment method
    notes = models.TextField(blank=True, null=True)  # Optional notes about the payment

    def __str__(self):
        # Return a readable string representation of the payment
        return f"Payment: ${self.amount} by {self.member} on {self.payment_date}"
