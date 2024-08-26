from django.contrib import admin
from .models import BlogPost, VersionPost
# Register your models here.
# class BlogPostAdmin(admin):

    
admin.site.register(BlogPost)
admin.site.register(VersionPost)