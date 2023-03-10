from apiv2.serializers import (
    PostListSerializer, 
    PostRetrieveSerializer, 
    PostSerializerDetail, 
    TagSerializer,
    )
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from api.models import Post, Category
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import OrderedDict
from django.views.generic.list import BaseListView
from django.db.models import Count
from .utils import make_tag_cloud, get_prev_next

class PostPageNumberPagination(PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    def get_paginated_response(self, data):
      return Response(OrderedDict([
          ('postList', data),
          ('pageCnt', self.page.paginator.num_pages),
          ('curPage', self.page.number),
      ]))

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

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

    def get_serializer_context(self):
      """
      Extra context provided to the serializer class.
      """
      return {
          'request': None,
          'format': self.format_kwarg,
          'view': self
      }


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        data = {
            'post': instance,
            'prevPost': prevInstance,
            'nextPost': nextInstance,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)
    
    def get_serializer_context(self):
      """
      Extra context provided to the serializer class.
      """
      return {
          'request': None,
          'format': self.format_kwarg,
          'view': self
      }

# class CateTagAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # cateList = Category.objects.all()
#         qs = Tag.objects.annotate(count=Count('post'))
#         tagList = make_tag_cloud(qs)
#         data = {
#             # 'cateList': cateList,
#             'tagList': tagList,
#         }

#         serializer = CateTagSerializer(instance=data)
#         return Response(serializer.data)

class TagCloudAPIView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Tag.objects.annotate(count=Count('post'))
        tagList = make_tag_cloud(qs)
        data = {
            'tagList': tagList,
        }

        serializer = TagSerializer(instance=data)
        return Response(serializer.data)