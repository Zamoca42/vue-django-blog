from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from pathlib import Path
from ckeditor_uploader.fields import RichTextUploadingField
from django.dispatch import receiver
from django.db.models.signals import post_delete
from taggit.models import TaggedItem

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    # tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField(verbose_name='TITLE', max_length=50)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    image = models.FileField('IMAGE', upload_to='blog/%Y/%m/', blank=True, null=True)
    content = models.TextField('CONTENT')
    # content = MDTextField()
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    tags = TaggableManager(blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='OWNER',default='zamoca')
    # like = models.PositiveSmallIntegerField('LIKE', default=0)

    class Meta:
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.id))
    
    def get_prev(self):
        return self.get_previous_by_modify_dt()
    
    def get_next(self):
        return self.get_next_by_modify_dt()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')

    def __str__(self):
        return self.name

@receiver(post_delete, sender=TaggedItem)
def delete_unused_tags(sender, instance, **kwargs):
    n_tagged = TaggedItem.objects.filter(tag_id=instance.tag_id).count()
    if n_tagged == 0:
        instance.tag.delete()