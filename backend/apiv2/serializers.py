from rest_framework import serializers
from api.models import Post, Category
from taggit.models import Tag
from django.conf import settings

# Serializers define the API representation.

class PostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    # tag_names = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True)
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')
    # image = serializers.SerializerMethodField()

    # def get_tag_names(self, obj):
    #     return [tag.name for tag in obj.tags.all()]
    
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['create_dt', 'content', 'owner']
    
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

class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    tags = serializers.StringRelatedField(many=True)
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')
    owner = serializers.StringRelatedField()

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['create_dt', 'image']

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

class TagSerializer(serializers.Serializer):
    # cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.DictField())