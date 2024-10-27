from rest_framework import serializers

from apps.course.models import Color


class ColorSerializer(serializers.ModelSerializer):
    hex_code = serializers.CharField(min_length=7, max_length=7)
    
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']
