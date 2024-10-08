# accounts/urls.py
from django.urls import path

from .views import SignUpView, PasswordChangeView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]