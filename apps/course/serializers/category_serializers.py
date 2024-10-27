from rest_framework import serializers

from apps.course.models import Category


class CategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'courses_count']

    @staticmethod
    def validate_name(value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value
