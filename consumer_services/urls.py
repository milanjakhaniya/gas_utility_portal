# consumer_services/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login,name='login'),
    path('submit_request/', views.submit_request, name='submit_request'),
    path('representative_dashboard/', views.representative_dashboard, name='representative_dashboard'),
    path('track_request/', views.track_request, name='track_request'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_representative/', views.register_representative, name='register_representative'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('editProfile/', views.editProfile, name='editProfile'),
]
