from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    MembershipTypeListView,
    MembershipTypeDetailView,
    MemberListView,
    MemberDetailView,
    PaymentListView,
    PaymentDetailView,
    CheckInListView,
    MemberCreateView,
    MemberUpdateView,
    register, 
    homepage,
    make_payment,
    create_checkin, CheckInHistoryView,
    workout_data, 

)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('membershiptypes/', MembershipTypeListView.as_view(), name='membershiptype_list'),
    path('membershiptypes/<int:pk>/', MembershipTypeDetailView.as_view(), name='membershiptype_detail'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member_detail'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('checkins/', CheckInListView.as_view(), name='checkin_list'),
    path('members/add/', MemberCreateView.as_view(), name='add_member'),
    path('members/<int:pk>/update/', MemberUpdateView.as_view(), name='update_member'),
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='project/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('members/make_payment/', make_payment, name='make_payment'),
    path('members/<int:pk>/checkin/', create_checkin, name='create_checkin'),
    path('members/<int:pk>/checkin_history/', CheckInHistoryView.as_view(), name='checkin_history'),
    path('members/<int:pk>/workout_data/', workout_data, name='workout_data'),
]
