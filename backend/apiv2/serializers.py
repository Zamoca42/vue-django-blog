from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Category
from taggit.models import Tag

# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

class PostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    image = serializers.ImageField(use_url='https://via.placeholder.com/900x300/', allow_empty_file=False)
    # tag_names = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True)
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')

    # def get_tag_names(self, obj):
    #     return [tag.name for tag in obj.tags.all()]
    
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['create_dt', 'content', 'owner']

class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    tags = serializers.StringRelatedField(many=True)
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')
    
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['create_dt', 'image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = '__all__'
        fields = ['name']

class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())

class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']

class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub()
    nextPost = PostSerializerSub()
    # category = serializers.CharField(source='category.name')

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['id','title','image','like','category']
