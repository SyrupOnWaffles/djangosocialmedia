from django.contrib import admin
from socialMedia.models import Post, UserProfile, Reply, Like, ReplyLike, Follow
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


class ReplyAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    pass

class FollowAdmin(admin.ModelAdmin):
    pass

class ReplyLikeAdmin(admin.ModelAdmin):
    pass



admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(ReplyLike, ReplyLikeAdmin)
admin.site.register(Follow, FollowAdmin)