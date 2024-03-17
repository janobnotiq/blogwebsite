from django.contrib import admin
from .models import Comment, Post

from unfold.admin import ModelAdmin

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["title","content","author","date_posted"]

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ["text","sender"]

