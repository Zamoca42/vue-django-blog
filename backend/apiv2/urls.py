from django.urls import path
from apiv2 import views

app_name = 'api2'

urlpatterns = [
    path('post/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),

    # path('category/', views.CateTagAPIView.as_view(), name='catetag'),
    # path('tag/cloud/', views.ApiTagCloudLV.as_view(), name='tag_cloud'),
]