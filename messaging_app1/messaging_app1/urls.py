# messaging_app1/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add a home route for the root URL
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
