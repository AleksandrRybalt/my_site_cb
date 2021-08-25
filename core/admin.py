from django.contrib import admin
from .models import *


class PostsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'time_create', 'is_published')
    list_display_links = ('title',)
    search_fields = ('id', 'title')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(PostsModel, PostsModelAdmin)
