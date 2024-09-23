from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('post/<int:pk>/',views.post_detail,name="post_detail"),
    path('profile/<int:pk>/',views.profile_detail,name="profile_detail"),
    path('paint/',views.create_post,name="create_post"),
    path('',views.post_homepage,name="home"),
]