from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'myapp.views.custom_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

