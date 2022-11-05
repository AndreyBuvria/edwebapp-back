from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from core.models import Role


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, email_value):
        if get_user_model().objects.filter(email=email_value):
            raise serializers.ValidationError('A user with that email already exists') 

        return email_value

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'role', 'about', 'password', 'date_joined',
                  'timecreate', 'is_superuser')

class UserReadSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'role', 'about', 'date_joined',
                  'timecreate', 'is_superuser')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['access_token_lifetime'] = str(int(refresh.access_token.lifetime.total_seconds() * 1000))
        data['refresh_token_lifetime'] = str(int(refresh.lifetime.total_seconds() * 1000))

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
