from rest_framework import serializers

from apps.info.models import Config


class ConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = ('key', 'value')
