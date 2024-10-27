from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.course.models import Course
from apps.info.models import Report
from apps.quiz.models import Quiz


class ReportSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(source='course.id', required=False)
    quiz_id = serializers.UUIDField(source='quiz.id', required=False)

    class Meta:
        model = Report
        fields = ('id', 'course_id', 'quiz_id', 'type', 'message', 'image', 'created_at',)

    def create(self, validated_data):
        course= validated_data.pop('course', None)
        quiz = validated_data.pop('quiz', None)
        report = Report.objects.create(**validated_data)
        if course:
            report.course = get_object_or_404(Course, id=course['id'])
        if quiz:
            report.quiz = get_object_or_404(Quiz, id=quiz['id'])
        report.save()
        return report
