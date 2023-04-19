
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from mysite.views import robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api2/', include('apiv2.urls')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
    path("robots.txt", robots_txt),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)