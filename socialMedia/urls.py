from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    # settings
    path("settings/", views.account_settings, name="account_settings"),

    # draw
    path('paint/',views.create_post,name="create_post"),
    path('paintpfp/',views.create_pfp,name="create_pfp"),
    path('paintbio/',views.create_bio,name="create_bio"),

    # delete
    path('post/delete/<int:pk>',views.delete_post,name="delete_post"),
    path('reply/delete/<int:pk>',views.delete_reply,name="delete_reply"),

    # post displays
    path('',views.post_homepage,name="home"),
    path('post/<int:pk>/',views.post_detail,name="post_detail"),
    path('profile/<int:pk>/',views.profile_detail,name="profile_detail"),

    # follows
    path('profile/follow/<int:pk>/',views.profile_follow,name="profile_follow"),
    path('profile/get/followers/<int:pk>',views.profile_get_followers,name="profile_get_followers"),

    # likes
    path('post/like/<int:pk>/',views.post_like,name="post_like"),
    path('post/get/likes/<int:pk>',views.post_get_likes,name="post_get_likes"),

    path('reply/like/<int:pk>/',views.reply_like,name="reply_like"),
    path('reply/get/likes/<int:pk>',views.reply_get_likes,name="reply_get_likes"),

    # search
    path('search/<username>/',views.profile_search,name="profile_search"),
]