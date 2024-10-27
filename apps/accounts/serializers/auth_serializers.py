from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(write_only=True, help_text='Phone number or email')
    password = PasswordField(write_only=True)
    refresh = serializers.CharField(read_only=True, min_length=200, max_length=300)
    access = serializers.CharField(read_only=True, min_length=200, max_length=300)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        if '@' in login:
            user = authenticate(email=login, password=password)
        else:
            user = User.objects.filter(phone_number=login).first()
            user = authenticate(email=user.email if user else None, password=password)

        if not user:
            raise AuthenticationFailed(detail='Invalid login or password')

        if not user.is_active:
            raise AuthenticationFailed(detail='User account is disabled')

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        update_last_login(None, user)
        return data

    @staticmethod
    def get_token(user) -> RefreshToken:
        return RefreshToken.for_user(user)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.FileField(write_only=True, required=False)
    is_assistant = serializers.BooleanField(write_only=True, required=False, default=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    refresh = serializers.CharField(read_only=True, min_length=200, max_length=300)
    access = serializers.CharField(read_only=True, min_length=200, max_length=300)

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'gender', 'profile_picture', 'is_assistant',
            'phone_number', 'refresh', 'access'
        )
        extra_kwargs = {
            'gender': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date'),
            gender=validated_data.get('gender'),
            profile_picture=validated_data.get('profile_picture'),
            is_assistant=validated_data.get('is_assistant', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        refresh: RefreshToken = RefreshToken.for_user(user)
        user.refresh = str(refresh)
        user.access = str(refresh.access_token)
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['refresh'] = instance.refresh
        ret['access'] = instance.access
        return ret


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, validators=[validate_password], min_length=8)
    password2 = serializers.CharField(required=True, min_length=8)

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user=user)
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'new_password': 'Password fields did not match'})
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['password'])
        user.save()
        return user
