from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.models import Contact
from apps.info.serializers.contact_serializers import ContactSerializer
from config.permissons import IsAdminOrReadOnly


class ContactListView(APIView):
    serializer_class = ContactSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @extend_schema(
        tags=['Contact'],
        responses={200: ContactSerializer(many=True)},
        description='Get all contacts'
    )
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Contact'],
        request=ContactSerializer,
        responses={201: ContactSerializer},
        description='Create new contact'
    )
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
