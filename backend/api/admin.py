from django.contrib import admin
from api.models import Post, Category
from django.db import models

# 'tag_list',
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'image', 'modify_dt',)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')