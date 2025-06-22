from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# Оставляем только медиа файлы для Django
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Для production медиа файлы тоже через Django
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
