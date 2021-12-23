from django.contrib import admin
from social.models import Post, PostImage, Comment, Notification, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Tag)