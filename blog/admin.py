from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_added')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category',
                    'author', 'date_posted')
    list_display_links = ('id', 'title')
    search_fields = ('name',)
    list_per_page = 20


# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Comment)
