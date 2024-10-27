from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'bio', 'profile_picture', 'birth_date'
        ]


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'profile_picture')


class TeacherSerializer(UserSerializer):
    course_count = serializers.SerializerMethodField(read_only=True)
    student_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'gender', 'profile_picture',
            'is_assistant', 'course_count', 'student_count'
        ]

    def get_course_count(self, obj) -> int:
        return obj.courses.count()

    def get_student_count(self, obj) -> int:
        return User.objects.filter(enrollments__course__teacher=obj).count()
