from apiv2.serializers import (
    PostListSerializer, 
    PostRetrieveSerializer, 
    # PostSerializerDetail, 
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

class PostPageNumberPagination(pagination.PageNumberPagination):
    page_size = 12
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny] # only test

    def get_queryset(self):
        tagname = self.request.GET.get('tagname')
        category = self.request.GET.get('category')
        if tagname:
            qs = Post.objects.filter(tags__name=tagname)
        elif category:
            qs = Post.objects.filter(category__name=category)
        else:
            qs = Post.objects.all()
        return qs

class PostRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer #PostSerializerDetail
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny] # only test

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # prev_post, next_post = get_prev_next(instance)
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
        
        # post_serializer = PostRetrieveSerializer(instance)
        # prev_post_serializer = PostSerializerSub(prev_post)
        # next_post_serializer = PostSerializerSub(next_post)

        return Response({
            'post': serializer.data,
            'prevPost': prev_post_serializer.data if prev_post_serializer else None,
            'nextPost': next_post_serializer.data if next_post_serializer else None,
        })

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     prevInstance, nextInstance = get_prev_next(instance)
    #     data = {
    #         'post': instance,
    #         'prevPost': prevInstance,
    #         'nextPost': nextInstance,
    #     }
    #     serializer = PostSerializerDetail(instance=data) # self.get_serializer(instance=data)
    #     return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # Check Owner
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