from rest_framework import serializers

from apps.banner.models import Banner
from config.utils import TimestampField


class BannerSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(min_value=0, max_value=100)
    created_at = TimestampField(read_only=True)

    class Meta:
        model = Banner
        fields = '__all__'
