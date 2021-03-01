from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as ft
from django.urls import include, path

from . import views

handler404 = views.page_not_found
handler500 = views.server_error

urlpatterns = [
    path('about-author/', views.author, name='author'),
    path('about-tech/', views.tech, name='tech'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('api.urls')),
    path('', include('food.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
