from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.info.models import FAQCategory, FAQ


class FAQCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQCategory
        fields = ('id', 'name')


class FAQSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = FAQCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'category', 'category_id',)

    def create(self, validated_data):
        category = get_object_or_404(FAQCategory, id=validated_data['category_id'])
        return FAQ.objects.create(category=category, **validated_data)

    def update(self, instance, validated_data):
        category = get_object_or_404(FAQCategory, id=validated_data['category_id'])
        instance.category = category
        return super().update(instance, validated_data)
