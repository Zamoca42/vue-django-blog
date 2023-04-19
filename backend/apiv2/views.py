from apiv2.serializers import (
    PostListSerializer, 
    PostRetrieveSerializer, 
    TagSerializer,
    PostSerializerSub,
    )
from apiv2.models import Post, Category
from taggit.models import Tag
from rest_framework import pagination, views, generics, permissions, status
from rest_framework.response import Response
from collections import OrderedDict
from django.db.models import Count
from .utils import make_tag_cloud
from django_filters import rest_framework as filters
import django_filters

class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__name')
    tagname = django_filters.CharFilter(field_name='tags__name')

    class Meta:
        model = Post
        fields = ['category', 'tagname']

class PostPageNumberPagination(pagination.PageNumberPagination):
    page_size = 12
  
    def get_paginated_response(self, data):
      return Response(OrderedDict([
          ('postList', data),
          ('pageCnt', self.page.paginator.num_pages),
          ('curPage', self.page.number),
      ]))

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    # permission_classes = [permissions.AllowAny] # only test
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

class PostRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
    # permission_classes = [permissions.AllowAny] # only test

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        try:
            prev_post = instance.get_prev()
            prev_post_serializer = PostSerializerSub(prev_post)
        except Post.DoesNotExist:
            prev_post_serializer = None

        try:
            next_post = instance.get_next()
            next_post_serializer = PostSerializerSub(next_post)
        except Post.DoesNotExist:
            next_post_serializer = None

        return Response({
            'post': serializer.data,
            'prevPost': prev_post_serializer.data if prev_post_serializer else None,
            'nextPost': next_post_serializer.data if next_post_serializer else None,
        })
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in ['PUT', 'PATCH', 'DELETE'] and request.user != obj.owner:
            self.permission_denied(request)
    

class TagCloudAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        qs = Tag.objects.annotate(count=Count('post'))
        tagList = make_tag_cloud(qs)
        data = {
            'tagList': tagList,
        }

        serializer = TagSerializer(instance=data)
        return Response(serializer.data)