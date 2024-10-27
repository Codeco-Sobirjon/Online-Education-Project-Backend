from django.urls import path

from .views import *

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('user/<uuid:user_id>/', UserProfileAPIView.as_view(), name='user-detail'),

    path('teachers/', TeacherListAPIView.as_view(), name='teacher-list'),
]
