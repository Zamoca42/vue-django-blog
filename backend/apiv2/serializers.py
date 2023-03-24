from rest_framework import serializers
from apiv2.models import Post, Category
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.conf import settings

# Serializers define the API representation.

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    # tag_names = serializers.SerializerMethodField()
    # tags = serializers.StringRelatedField(many=True, required=False)
    tags = TagListSerializerField(required=False)
    # tags = TagListSerializerField(many=True)
    modify_dt = serializers.DateTimeField(format='%B %d, %Y', read_only=True)
    # image = serializers.SerializerMethodField()

    # def get_tag_names(self, obj):
    #     return [tag.name for tag in obj.tags.all()]
    
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ['create_dt', 'content', 'owner']

    def create(self, validated_data):
        category_name = validated_data.pop('category')['name']
        category, _ = Category.objects.get_or_create(name=category_name)
        
        # Extract and remove tags from validated_data
        tags = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        # post = Post.objects.create(category=category, **validated_data)

        return instance

    def to_representation(self, instance):
       representation = super().to_representation(instance)
    
       request = self.context.get('request')
    
       # Remove the specified fields for GET requests
       if request and request.method == 'GET':
           fields_to_omit = ['content', 'owner','create_dt']
           for field in fields_to_omit:
               representation.pop(field, None)
       return representation

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request')
    #     if request is not None:
    #         image_url = representation.get('image')
    #         representation['image'] = request.build_absolute_uri(image_url)
    #     else:
    #         representation['image'] = null
    #     return representation

    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         server_url = request.META.get('HTTP_HOST', settings.SERVER_URL)
    #         return 'http://{}/{}'.format(server_url, obj.image.url)
    #     else:
    #         return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         server_url = request.META.get('HTTP_HOST', settings.SERVER_URL)
    #         protocol = 'https' if request.is_secure() else 'http'
    #         return f"{protocol}://{server_url}{obj.image.url}"
    #     else:
    #         return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         server_url = request.META.get('HTTP_HOST', settings.SERVER_URL)
    #         if request.is_secure():
    #             return f'https://{server_url}{obj.image.url}'
    #         else:
    #             return f'http://{server_url}{obj.image.url}'
    #     else:
    #         return None

class PostRetrieveSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = CategorySerializer() # serializers.CharField(source='category.name', default='New')
    tags = serializers.StringRelatedField(many=True)
    #tags = TagListSerializerField()
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')
    owner = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'

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
        fields = '__all__'
        fields = ['post', 'prevPost', 'nextPost']


class TagSerializer(serializers.Serializer):
    # cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.DictField())