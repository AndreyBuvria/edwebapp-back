from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from course_api.models import CourseModel
from course_api.serializers import CourseSerializer


class RoleVerifySerializer(serializers.Serializer):
    access = serializers.CharField()

    def validate(self, attrs):
        token = AccessToken(attrs['access'], True)
        user_id = token['user_id']
        user = get_user_model().objects.get(id=user_id)
        role_name = [role_name for [pk, role_name] in get_user_model().USER_LEVEL_CHOICES if pk is user.role][0].upper()
        return { 'role': role_name }

class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

class UserSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=get_user_model().USER_LEVEL_CHOICES)

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
                  'timecreate', 'is_superuser',)


class UserReadSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=get_user_model().USER_LEVEL_CHOICES)
    #courses = serializers.PrimaryKeyRelatedField(queryset=CourseModel.objects.all(), many=True)
    #courses = CourseSerializer()

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'role', 'about', 'date_joined',
                  'timecreate', 'is_superuser')
        depth = 1 
