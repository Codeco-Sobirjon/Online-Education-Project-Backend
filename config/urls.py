from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from config.handlers import *

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),

    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.course.urls')),
    path('api/', include('apps.quiz.urls')),
    path('api/', include('apps.review.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.notification.urls')),
    path('api/', include('apps.banner.urls')),
    path('api/', include('apps.info.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler400 = handler400_view
handler404 = handler404_view
handler500 = handler500_view
