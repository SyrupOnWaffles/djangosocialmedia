from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid 
import os 

class Post(models.Model):
    body = models.ImageField()
    created_by = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.body.path)

class Reply(models.Model):
    body = models.ImageField()
    created_by = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE,related_name='replys')
    def __str__(self):
        return os.path.basename(self.body.path)

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE,related_name='likes')
    created_by = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['created_by', 'post'], name="unique_like"),
        ]

class ReplyLike(models.Model):
    reply = models.ForeignKey("Reply", on_delete=models.CASCADE,related_name='reply_likes')
    created_by = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['created_by', 'reply'], name="unique_reply_like"),
        ]

class Follow(models.Model):
    follow_to = models.ForeignKey("UserProfile", on_delete=models.CASCADE,related_name='followers')
    created_by = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['created_by', 'follow_to'], name="unique_follow"),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(default="placeholders/fpfPlaceholder.png")
    bio_picture = models.ImageField(default="placeholders/bioPlaceholder.png")

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 