from apiv2.serializers import (
    PostListSerializer, 
    PostRetrieveSerializer, 
    PostSerializerDetail, 
    TagSerializer,
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from apiv2.models import Post, Category
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from collections import OrderedDict
from django.db.models import Count
from .utils import make_tag_cloud, get_prev_next

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

class PostListAPIView(ModelViewSet):
    # TODO: Create
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    
    def get_actions(self):
        actions = super().get_actions()
        allowed_actions = ['list', 'create']
        return {key: actions[key] for key in actions if key in allowed_actions}


class PostRetrieveAPIView(ModelViewSet):
    # TODO: Retrieve. Update. Delete
    queryset = Post.objects.all()
    serializer_class = PostSerializerDetail
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    
    def get_actions(self):
        actions = super().get_actions()
        allowed_actions = ['retrieve', 'update', 'partial_update', 'destroy']
        return {key: actions[key] for key in actions if key in allowed_actions}

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