from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer, NotificationListSerializer
from config.permissons import IsAuth, IsAdminOrAuth


class NotificationView(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = IsAdminOrAuth,

    @extend_schema(
        tags=['Notification'],
        responses={200: serializer_class(many=True)},
        description='Get all notifications for user'
    )
    def get(self, request):
        notifications = request.user.notifications.all()
        serializer = self.serializer_class(notifications, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Notification'],
        request=NotificationSerializer,
        responses={201: OpenApiResponse(description='Notification created successfully and sent all users')},
        description='Create notification and send to all users'
    )
    def post(self, request):
        serializer = NotificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'message': 'Notification created successfully and sent all users'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailView(APIView):
    serializer_class = NotificationSerializer
    permission_classes = IsAuth,

    @extend_schema(
        tags=['Notification'],
        responses={200: serializer_class()},
        description='Get notification for user'
    )
    def get(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        serializer = self.serializer_class(notification, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
