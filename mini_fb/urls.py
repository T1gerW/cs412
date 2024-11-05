#mini_fb/urls.py
## description: URL patterns for the mini_fb app 

from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from . import views ## From . means from current directory 
from django.conf.urls.static import static

# all of the URLS that are part of this app 
urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name = "show_all_profiles"),
    path(r'profile/', views.ShowProfilePageView.as_view(), name = "show_profile"),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='view_profile'),
    path(r'create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'status/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path(r'profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/delete/<int:pk>/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/update/<int:pk>/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path(r'profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
    path(r'profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path(r'profile/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path(r'login/', views.CustomLoginView.as_view(), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),

    ##path(r'about', view.home, name = "about")

] + static(settings.STATIC_URL,
           document_root = settings.STATIC_ROOT)
