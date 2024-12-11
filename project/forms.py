from django import forms
from .models import Member, MembershipType, Payment
from django.contrib.auth.models import User
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # Handles months addition properly
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'required': 'required'}),
            'email': forms.EmailInput(attrs={'required': 'required'}),
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'last_name': forms.TextInput(attrs={'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number', 'membership_type']
        widgets = {
            'phone_number': forms.TextInput(attrs={'required': 'required'}),
            'membership_type': forms.Select(attrs={'required': 'required'}),
        }
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['member', 'payment_method', 'amount']

    def __init__(self, *args, is_superuser=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_superuser:
            self.fields.pop('member')  # Remove member field for non-superusers
