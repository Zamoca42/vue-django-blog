from rest_framework import serializers
from apiv2.models import Post, Category
from taggit.models import Tag
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.conf import settings

# Serializers define the API representation.

class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    tags = TagListSerializerField()
    create_dt = serializers.DateTimeField(format='%B %d, %Y')


    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        category_name = validated_data.pop('category')['name']
        category, _ = Category.objects.get_or_create(name=category_name)
        
        tags = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        instance.tags.set(*tags)

        return instance

    def to_representation(self, instance):
       representation = super().to_representation(instance)
    
       request = self.context.get('request')
    
       if request and request.method == 'GET':
           fields_to_omit = ['content', 'owner','modify_dt']
           for field in fields_to_omit:
               representation.pop(field, None)
       return representation

class PostRetrieveSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', default='New')
    tags = TagListSerializerField()
    modify_dt = serializers.DateTimeField(format='%B %d, %Y')
    create_dt = serializers.DateTimeField(format='%B %d, %Y')
    owner = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'create_dt', 'modify_dt', 'owner']

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)

        if category_data:
            category_name = category_data['name']
            category, created = Category.objects.get_or_create(name=category_name)
            instance.category = category

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
    
    def to_representation(self, instance):
       representation = super().to_representation(instance)
    
       request = self.context.get('request')
    
       if request and request.method == 'GET':
           fields_to_omit = ['description','image']
           for field in fields_to_omit:
               representation.pop(field, None)
       return representation

class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']

class TagSerializer(serializers.Serializer):
    tagList = serializers.ListField(child=serializers.DictField())