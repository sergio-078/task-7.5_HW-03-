from django.contrib import admin
from .models import Author, Category, Post, Comment, Subscriber
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscriber)
