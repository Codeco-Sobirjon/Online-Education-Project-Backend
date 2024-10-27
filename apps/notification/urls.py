from django.urls import path

from apps.notification.views import NotificationView, NotificationDetailView

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notification-list'),
    path('notifications/<uuid:notification_id>/', NotificationDetailView.as_view(), name='notification-detail'),
]

