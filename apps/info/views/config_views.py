from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.info.models import Config
from apps.info.serializers.config_serializers import ConfigSerializer
from config.permissons import IsAdmin


class ConfigListView(APIView):
    serializer_class = ConfigSerializer
    permission_classes = IsAdmin,

    @extend_schema(
        tags=['Config'],
        responses={200: ConfigSerializer(many=True)},
        description='Get all configs'
    )
    def get(self, request):
        configs = Config.objects.all()
        serializer = ConfigSerializer(configs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Config'],
        responses={201: ConfigSerializer(many=True)},
        description='Create new config'
    )
    def post(self, request):
        serialzer = ConfigSerializer(data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(serialzer.data, status=status.HTTP_201_CREATED)


class ConfigDetailView(APIView):
    serializer_class = ConfigSerializer
    permission_classes = IsAdmin,

    @extend_schema(
        tags=['Config'],
        responses={200: ConfigSerializer},
        description='Get config by key'
    )
    def get(self, request, key):
        config = Config.objects.get(key=key)
        serializer = ConfigSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Config'],
        responses={200: ConfigSerializer},
        description='Update config by key'
    )
    def put(self, request, key):
        config = Config.objects.get(key=key)
        serialzer = ConfigSerializer(config, data=request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(serialzer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Config'],
        description='Delete config by key'
    )
    def delete(self, request, key):
        config = Config.objects.get(key=key)
        config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
