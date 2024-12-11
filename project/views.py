from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import MembershipType, Member, CheckIn, Payment
from .forms import MemberForm, PaymentForm, UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseForbidden
from django.db import IntegrityError
from datetime import date

# ListView for displaying all membership types
class MembershipTypeListView(ListView):
    model = MembershipType
    template_name = 'project/membershiptype_list.html'  # Template for listing membership types

# DetailView for displaying details of a single membership type
class MembershipTypeDetailView(DetailView):
    model = MembershipType
    template_name = 'project/membershiptype_detail.html'  # Template for membership type details

# ListView for displaying all members (restricted to superusers)
class MemberListView(ListView):
    model = Member
    template_name = 'project/member_list.html'
    context_object_name = 'members'  # Name used in the template for the list of members

    def test_func(self):
        # Restrict access to superusers
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect non-superusers to their own member detail page
        if self.request.user.is_authenticated:
            try:
                return redirect('member_detail', pk=self.request.user.member.pk)
            except Member.DoesNotExist:
                return redirect('homepage')
        else:
            return super().handle_no_permission()

# DetailView for displaying details of a single member
class MemberDetailView(DetailView):
    model = Member
    template_name = 'project/member_detail.html'  # Template for member details

    def get_queryset(self):
        # Superusers can view all members, users can view only their own details
        if self.request.user.is_superuser:
            return Member.objects.all()
        else:
            return Member.objects.filter(email=self.request.user.email)

# UpdateView for updating member information
class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'project/update_member.html'  # Template for updating member information

    def get_success_url(self):
        # Redirect to the member's detail page after update
        return reverse('member_detail', kwargs={'pk': self.object.pk})

# ListView for displaying all payments
class PaymentListView(ListView):
    model = Payment
    template_name = 'project/payment_list.html'  # Template for listing payments

# DetailView for displaying details of a single payment
class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'project/payment_detail.html'  # Template for payment details

# ListView for displaying all check-ins (paginated)
class CheckInListView(ListView):
    model = CheckIn
    template_name = 'project/checkin.html'  # Template for listing check-ins
    context_object_name = 'checkins'  # Name used in the template for the list of check-ins
    ordering = ['-check_in_date']  # Order check-ins by most recent first
    paginate_by = 10  # Display 10 check-ins per page

# CreateView for creating a new member
class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'project/add_member.html'  # Template for adding a new member
    success_url = reverse_lazy('member_list')  # Redirect to the member list after successful creation

# Function-based view for user registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        member_form = MemberForm(request.POST, request.FILES)
        if user_form.is_valid() and member_form.is_valid():
            # Create the user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create the associated member if it doesn't already exist
            if not hasattr(user, 'member'):
                member = member_form.save(commit=False)
                member.user = user
                member.email = user.email
                member.first_name = user.first_name
                member.last_name = user.last_name
                member.join_date = date.today()
                if member.membership_type:
                    member.expiration_date = date.today() + relativedelta(months=member.membership_type.duration)
                member.save()

            return redirect('login')  # Redirect to login page after registration
    else:
        user_form = UserRegistrationForm()
        member_form = MemberForm()

    return render(request, 'project/register.html', {'user_form': user_form, 'member_form': member_form})

# Redirect users to their appropriate homepage based on user type
@login_required
def homepage(request):
    if request.user.is_superuser:
        return redirect('member_list')  # Superusers see the member list
    else:
        try:
            return redirect('member_detail', pk=request.user.member.pk)  # Users see their own details
        except Member.DoesNotExist:
            return HttpResponseForbidden("You do not have a member profile assigned.")  # Handle missing profile

# Function-based view for making a payment
@login_required
def make_payment(request):
    try:
        member = request.user.member  # Get the logged-in user's member profile
    except Member.DoesNotExist:
        return render(request, 'project/no_profile.html', {'message': "You do not have a member profile."})

    if request.method == 'POST':
        form = PaymentForm(request.POST, is_superuser=request.user.is_superuser)
        if form.is_valid():
            payment = form.save(commit=False)
            if not request.user.is_superuser:
                payment.member = member  # Associate payment with the logged-in user
            payment.save()
            return redirect('member_detail', pk=member.pk)  # Redirect to the member's detail page
    else:
        form = PaymentForm(is_superuser=request.user.is_superuser)

    return render(request, 'project/make_payment.html', {'form': form, 'member': member})

# Function-based view for creating a check-in instance
@login_required
def create_checkin(request, pk):
    member = get_object_or_404(Member, pk=pk)  # Retrieve the member by primary key
    if not (request.user.is_superuser or request.user == member.user):
        return redirect('member_detail', pk=pk)  # Restrict access to the member or admin
    CheckIn.objects.create(member=member)  # Create a new check-in for the member
    return redirect('member_detail', pk=pk)  # Redirect to the member's detail page

# ListView for displaying a member's check-in history
class CheckInHistoryView(ListView):
    model = CheckIn
    template_name = 'project/checkin_hist.html'  # Template for check-in history
    context_object_name = 'checkins'
    paginate_by = 5  # Show 5 check-ins per page

    def get_queryset(self):
        # Filter check-ins by the member's primary key
        return CheckIn.objects.filter(member_id=self.kwargs['pk']).order_by('-check_in_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = get_object_or_404(Member, pk=self.kwargs['pk'])  # Retrieve the member explicitly
        return context

# Function-based view for displaying workout data and weekly insights
def workout_data(request, pk):
    member = get_object_or_404(Member, pk=pk)  # Retrieve the member by primary key
    checkins = CheckIn.objects.filter(member=member)  # Get all check-ins for the member
    total_checkins = checkins.count()

    if total_checkins == 0:
        message = "We await your first visit!"  # Message for no check-ins
    else:
        earliest_checkin = checkins.order_by('check_in_date').first().check_in_date
        weeks_active = max((now() - earliest_checkin).days / 7, 1)
        avg_weekly_checkins = total_checkins / weeks_active

        today = now()
        start_of_this_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timedelta(weeks=1)
        end_of_last_week = start_of_this_week

        this_week_checkins = checkins.filter(check_in_date__gte=start_of_this_week).count()
        last_week_checkins = checkins.filter(check_in_date__gte=start_of_last_week, check_in_date__lt=end_of_last_week).count()

        if this_week_checkins == last_week_checkins:
            message = "It's been a while since you've visited us. We MISS you!" if this_week_checkins == 0 else "You've hit the same number of workouts as last week! Consistent!"
        elif this_week_checkins > last_week_checkins:
            message = "You've worked out with us more than last week! Keep it up!"
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
    return render(request, 'project/workout_data.html', context)  # Render the workout data page