from apiv2.serializers import PostListSerializer, PostRetrieveSerializer, CateTagSerializer, PostSerializerDetail 
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from api.models import Post, Category
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import OrderedDict

class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            'cateList': cateList,
            'tagList': tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)

class PostPageNumberPagination(PageNumberPagination):
    page_size = 12
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

    def get_serializer_context(self):
      """
      Extra context provided to the serializer class.
      """
      return {
          'request': None,
          'format': self.format_kwarg,
          'view': self
      }

def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_modify_dt()
    except instance.DoesNotExist:
        prev = None
    
    try:
        next_ = instance.get_next_by_modify_dt()
    except instance.DoesNotExist:
        next_ = None
    
    return prev, next_

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
