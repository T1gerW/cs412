from django import forms
from .models import Member, MembershipType, Payment  # Import models used for the forms
from django.contrib.auth.models import User  # Import Django's built-in User model
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # Helps with handling date calculations, especially months

# Form for user registration
class UserRegistrationForm(forms.ModelForm):
    """
    A form for registering new users, including password confirmation.
    Extends Django's built-in ModelForm for the User model.
    """
    password = forms.CharField(
        widget=forms.PasswordInput,  # Use a password input widget for security
        required=True,
        label="Password"  # Label displayed on the form
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,  # Use a password input widget for confirmation
        required=True,
        label="Confirm Password"
    )

    class Meta:
        """
        Metadata for the form, defining the User model and the fields to be included.
        """
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Fields displayed on the registration form
        widgets = {
            'username': forms.TextInput(attrs={'required': 'required'}),  # Mark username as required
            'email': forms.EmailInput(attrs={'required': 'required'}),  # Mark email as required
            'first_name': forms.TextInput(attrs={'required': 'required'}),  # Mark first name as required
            'last_name': forms.TextInput(attrs={'required': 'required'}),  # Mark last name as required
        }

    def clean(self):
        """
        Custom validation to ensure that the password and confirm_password fields match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")  # Raise an error if passwords don't match

        return cleaned_data  # Return the cleaned data if validation passes

# Form for creating or updating a member
class MemberForm(forms.ModelForm):
    """
    A form for creating or updating a Member instance.
    Allows input for phone number and membership type.
    """
    class Meta:
        """
        Metadata for the form, defining the Member model and the fields to be included.
        """
        model = Member
        fields = ['phone_number', 'membership_type']  # Fields displayed on the form
        widgets = {
            'phone_number': forms.TextInput(attrs={'required': 'required'}),  # Mark phone number as required
            'membership_type': forms.Select(attrs={'required': 'required'}),  # Mark membership type as required
        }

# Form for processing payments
class PaymentForm(forms.ModelForm):
    """
    A form for creating Payment instances, with optional customization for superusers.
    """
    class Meta:
        """
        Metadata for the form, defining the Payment model and the fields to be included.
        """
        model = Payment
        fields = ['member', 'payment_method', 'amount']  # Fields displayed on the payment form

    def __init__(self, *args, is_superuser=False, **kwargs):
        """
        Customize the form to exclude the 'member' field for non-superusers.
        Args:
            is_superuser (bool): Determines whether the 'member' field is displayed.
        """
        super().__init__(*args, **kwargs)
        if not is_superuser:
            self.fields.pop('member')  # Remove the member field for non-superusers
