from django.contrib.auth import login, logout, update_session_auth_hash, get_user
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDeleteView
from django.views.generic.list import BaseListView
from taggit.models import Tag

from django.http import JsonResponse
# from django.db.models import Count
from blog.models import Post
from taggit.models import Tag
from api.views_util import obj_to_post, prev_next_post, make_tag_cloud

class ApiPostLV(BaseListView):
    #model = Post
    def get_queryset(self):
        tagname = self.request.GET.get('tagname')
        if tagname:
            qs = Post.objects.filter(tags__name=tagname)
        else:
            qs = Post.objects.all()
        return qs
    
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        postList = [obj_to_post(obj) for obj in qs]
        return JsonResponse(data=postList, safe=False, status=200)

class ApiPostDV(BaseDetailView):
    model = Post

    def render_to_response(self, context, **response_kwargs):
        obj = context['object']
        post = obj_to_post(obj)
        post['prev'], post['next'] = prev_next_post(obj)
        return JsonResponse(data=post, safe=True, status=200)

class ApiTagCloudLV(BaseListView):
    queryset = Tag.objects.annotate(count=Count('post'))
    
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        tagList = make_tag_cloud(qs)
        return JsonResponse(data=tagList, safe=False, status=200)