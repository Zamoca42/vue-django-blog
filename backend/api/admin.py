from django.contrib import admin

from api.models import Post, Category
from django.db import models
# from markdownx.widgets import AdminMarkdownxWidget
from martor.widgets import AdminMartorWidget

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'image', 'modify_dt', 'tag_list')
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMarkdownxWidget},
    # }
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')