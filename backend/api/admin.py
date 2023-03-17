from django.contrib import admin
from api.models import Post, Category
from django.db import models
from django import forms
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_ckeditor_5.widgets import CKEditor5Widget

# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = Post
#         fields = '__all__'

class contentForm(forms.ModelForm):

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["content"].required = False

      class Meta:
          model = Post
          fields = ("content",)
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )
          }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'image', 'modify_dt',)
    # form = contentForm

    def get_queryset(self, request):
        return super().get_queryset(request)

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')