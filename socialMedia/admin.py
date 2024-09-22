from django.contrib import admin
from socialMedia.models import Post, UserProfile, Reply
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass


class ReplyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reply, ReplyAdmin)