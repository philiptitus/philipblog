from django.contrib import admin
from articles.models import Article,Bookmark,Like
from posts.models import  Post
from groups.models import Group,GroupMember

# Register your models here.
admin.site.register(Article)
admin.site.register(Bookmark)
admin.site.register(Like)






