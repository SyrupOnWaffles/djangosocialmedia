from django.contrib import admin
from socialMedia.models import Post, UserProfile, Reply, Like
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


class ReplyAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Like, LikeAdmin)