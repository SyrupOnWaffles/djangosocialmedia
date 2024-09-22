from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('post/<int:pk>/',views.post_detail,name="post_detail"),
    path('profile/<int:pk>/',views.profile_detail,name="profile_detail"),
    path('paint/',views.paint,name="paint"),
    path('',views.post_homepage,name="home"),
]