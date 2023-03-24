from apiv2.serializers import (
    PostListSerializer, 
    PostRetrieveSerializer, 
    PostSerializerDetail, 
    TagSerializer,
    PostSerializerSub,
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from apiv2.models import Post, Category
from taggit.models import Tag
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from collections import OrderedDict
from django.db.models import Count
from .utils import make_tag_cloud, get_prev_next
from rest_framework import status

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

class PostListAPIView(ListCreateAPIView):
    # TODO: Create. List
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

class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    # TODO: Retrieve. Update. Delete
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer #PostSerializerDetail
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        prevInstance, nextInstance = get_prev_next(instance)
        data = {
            'post': instance,
            'prevPost': prevInstance,
            'nextPost': nextInstance,
        }
        serializer = PostSerializerDetail(instance=data) # self.get_serializer(instance=data)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            prevInstance, nextInstance = get_prev_next(instance)
            data = {
                'post': serializer.data,
                'prevPost': prevInstance,
                'nextPost': nextInstance,
            }
            response_serializer = PostSerializerDetail(instance=data) # self.get_serializer(instance=data)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagCloudAPIView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Tag.objects.annotate(count=Count('post'))
        tagList = make_tag_cloud(qs)
        data = {
            'tagList': tagList,
        }

        serializer = TagSerializer(instance=data)
        return Response(serializer.data)