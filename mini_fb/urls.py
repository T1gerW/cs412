#mini_fb/urls.py
## description: URL patterns for the mini_fb app 

from django.urls import path 
from django.conf import settings
from . import views ## From . means from current directory 
from django.conf.urls.static import static

# all of the URLS that are part of this app 
urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name = "show_all_profiles"),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name = "show_profile"),
    path(r'create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path(r'profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path(r'profile/<int:pk>/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
    path(r'profile/<int:pk>/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path(r'profile/<int:pk>/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),

    ##path(r'about', view.home, name = "about")

] + static(settings.STATIC_URL,
           document_root = settings.STATIC_ROOT)
