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
    name = models.CharField(max_length=100)  # e.g., Monthly, Yearly
    duration = models.PositiveIntegerField(help_text="Duration in months")  # Membership duration
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Membership cost
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.name} ({self.duration} months - ${self.price})"

# Model for Member
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default= "None")
    membership_type = models.ForeignKey('MembershipType', on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def calculate_expiration_date(self):
        if self.membership_type:
            return date.today() + relativedelta(months=self.membership_type.duration)
        return None

    def last_payment_date(self):
        latest_payment = Payment.objects.filter(member=self).aggregate(latest=Max('payment_date'))['latest']
        return latest_payment if latest_payment else "No payments made"

@receiver(pre_save, sender=Member)
def set_expiration_date(sender, instance, **kwargs):
    if not instance.expiration_date:
        instance.expiration_date = instance.calculate_expiration_date()


# Model for Member Check-Ins
class CheckIn(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='checkins')
    check_in_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check-In: {self.member} on {self.check_in_date}"


# Model for Payments
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # Associate payment with a member
    payment_date = models.DateField(auto_now_add=True)  # Automatically set when a payment is made
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='credit_card')
    notes = models.TextField(blank=True, null=True)  # Optional notes about the payment

    def __str__(self):
        return f"Payment: ${self.amount} by {self.member} on {self.payment_date}"

