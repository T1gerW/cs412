from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import MembershipType, Member, CheckIn, Payment, CheckIn
from .forms import MemberForm, PaymentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm, MemberForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.utils.timezone import now, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# ListView for Membership Types
class MembershipTypeListView(ListView):
    model = MembershipType
    template_name = 'project/membershiptype_list.html'  # Template for listing membership types

# DetailView for Membership Types
class MembershipTypeDetailView(DetailView):
    model = MembershipType
    template_name = 'project/membershiptype_detail.html'  # Template for membership type details


# ListView for Members
class MemberListView(ListView):
    model = Member
    template_name = 'project/member_list.html'  # Template for listing members
    context_object_name = 'members'

    def test_func(self):
        # Only allow superusers (admins) to access this view
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect regular users to their member detail page or homepage
        if self.request.user.is_authenticated:
            try:
                return redirect('member_detail', pk=self.request.user.member.pk)
            except Member.DoesNotExist:
                return redirect('homepage')
        else:
            return super().handle_no_permission()

# DetailView for Members
class MemberDetailView(DetailView):
    model = Member
    template_name = 'project/member_detail.html'  # Template for member details

    def get_queryset(self):
        if self.request.user.is_superuser:  # Admin can view all members
            return Member.objects.all()
        else:  # Regular user can only view their own details
            return Member.objects.filter(email=self.request.user.email)

class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'project/update_member.html'

    def get_success_url(self):
        # Redirect to the member detail page of the current member
        return reverse('member_detail', kwargs={'pk': self.object.pk})


# ListView for Payments
class PaymentListView(ListView):
    model = Payment
    template_name = 'project/payment_list.html'  # Template for listing payments


# DetailView for Payments
class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'project/payment_detail.html'  # Template for payment details

class CheckInListView(ListView):
    model = CheckIn
    template_name = 'project/checkin.html'  # Template for listing check-ins
    context_object_name = 'checkins'  # Name for use in the template
    ordering = ['-check_in_date']  # Order by most recent check-in first
    paginate_by = 10  # Display 10 check-ins per page

class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'project/add_member.html'
    success_url = reverse_lazy('member_list')  # Redirect to the member list after successful creation

class MembershipTypeListView(LoginRequiredMixin, ListView):
    model = MembershipType
    template_name = 'project/membershiptype_list.html'
    context_object_name = 'membershiptypes'

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        member_form = MemberForm(request.POST, request.FILES)
        if user_form.is_valid() and member_form.is_valid():
            # Create the User
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Check if a Member already exists
            if not hasattr(user, 'member'):
                # Create the Member associated with the User
                member = member_form.save(commit=False)
                member.user = user
                member.email = user.email  # Match the email
                member.first_name = user.first_name
                member.last_name = user.last_name
                member.join_date = date.today()
                if member.membership_type:
                    member.expiration_date = date.today() + relativedelta(months=member.membership_type.duration)
                member.save()

            # Redirect to login after successful registration
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        member_form = MemberForm()

    return render(request, 'project/register.html', {'user_form': user_form, 'member_form': member_form})










@login_required
def homepage(request):
    if request.user.is_superuser:
        # Admin: redirect to the member list page
        return redirect('member_list')
    else:
        # Regular user: redirect to their member detail page
        try:
            return redirect('member_detail', pk=request.user.member.pk)
        except Member.DoesNotExist:
            # Handle case where the user has no associated Member profile
            return HttpResponseForbidden("You do not have a member profile assigned.")
        
@login_required
def make_payment(request):
    # Get the current user's member profile
    try:
        member = request.user.member
    except Member.DoesNotExist:
        return render(request, 'project/no_profile.html', {'message': "You do not have a member profile."})

    if request.method == 'POST':
        form = PaymentForm(request.POST, is_superuser=request.user.is_superuser)
        if form.is_valid():
            payment = form.save(commit=False)
            # For non-superusers, default to their associated member
            if not request.user.is_superuser:
                payment.member = member
            payment.save()
            return redirect('member_detail', pk=member.pk)
    else:
        form = PaymentForm(is_superuser=request.user.is_superuser)

    return render(request, 'project/make_payment.html', {'form': form, 'member': member})

@login_required
def create_checkin(request, pk):
    member = get_object_or_404(Member, pk=pk)

    # Ensure only the member or an admin can create a check-in
    if not (request.user.is_superuser or request.user == member.user):
        return redirect('member_detail', pk=pk)

    # Create the check-in instance
    CheckIn.objects.create(member=member)
    return redirect('member_detail', pk=pk)

class CheckInHistoryView(ListView):
    model = CheckIn
    template_name = 'project/checkin_hist.html'
    context_object_name = 'checkins'
    paginate_by = 5  # Show 5 check-ins per page

    def get_queryset(self):
        member_id = self.kwargs['pk']
        return CheckIn.objects.filter(member_id=member_id).order_by('-check_in_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the member explicitly
        context['member'] = get_object_or_404(Member, pk=self.kwargs['pk'])
        return context
    
def workout_data(request, pk):
    # Retrieve the member
    member = get_object_or_404(Member, pk=pk)

    # Get all check-ins for this member
    checkins = CheckIn.objects.filter(member=member)

    # Calculate total check-ins
    total_checkins = checkins.count()

    # Handle case where no check-ins have been made
    if total_checkins == 0:
        message = "We await your first visit!"
    else:
        # Calculate average weekly check-ins
        earliest_checkin = checkins.order_by('check_in_date').first().check_in_date
        weeks_active = max((now() - earliest_checkin).days / 7, 1)
        avg_weekly_checkins = total_checkins / weeks_active

        # Calculate check-ins this week and last week
        today = now()
        start_of_this_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timedelta(weeks=1)
        end_of_last_week = start_of_this_week

        this_week_checkins = checkins.filter(check_in_date__gte=start_of_this_week).count()
        last_week_checkins = checkins.filter(check_in_date__gte=start_of_last_week, check_in_date__lt=end_of_last_week).count()

        # Determine the message
        if this_week_checkins == last_week_checkins:
            if this_week_checkins == 0:
                message = "It's been a while since you've visited us. We MISS you!"
            else:
                message = "You've hit the same number of workouts with us as you have last week! Consistent!"
        elif this_week_checkins > last_week_checkins:
            message = "You've worked out with us more than you have last week! Keep it up!"
        else:
            message = f"You've only hit {this_week_checkins} compared to {last_week_checkins} workouts last week. Keep going!"

    context = {
        'member': member,
        'total_checkins': total_checkins,
        'avg_weekly_checkins': avg_weekly_checkins if total_checkins > 0 else 0,
        'this_week_checkins': this_week_checkins if total_checkins > 0 else 0,
        'last_week_checkins': last_week_checkins if total_checkins > 0 else 0,
        'message': message,
    }
    return render(request, 'project/workout_data.html', context)


