from django.urls import path

from apps.banner.views import BannerView

urlpatterns = [
    path('banners/', BannerView.as_view(), name='banner-list'),
]
