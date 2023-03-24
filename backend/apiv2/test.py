from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apiv2.models import Post, Category
from accounts.models import User
from taggit.models import Tag
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Test Category')
        # self.tag1 = Tag.objects.create(name='Test Tag 1')
        # self.tag2 = Tag.objects.create(name='Test Tag 2')

        self.post = Post.objects.create(
            category=self.category,
            title='Test Post',
            description='This is a test post',
            content='This is the content of the test post',
        )
        # self.post.tags.add(self.tag1)
        # self.post.tags.add(self.tag2)

    def test_create_post(self):
        url = reverse_lazy('api2:post-list')
        data = {
            'category': self.category.id,
            'title': 'New Post',
            'description': 'This is a new post',
            'content': 'This is the content of the new post',
            # 'tags': [self.tag1.id, self.tag2.id],
        }
        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, 'New Post')

    def test_retrieve_post(self):
        url = reverse_lazy('api2:post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_update_post(self):
        url = reverse_lazy('api2:post-detail', args=[self.post.id])
        data = {'title': 'Updated Post'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, 'Updated Post')

    def test_delete_post(self):
        url = reverse_lazy('api2:post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
