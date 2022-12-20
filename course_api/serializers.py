from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CourseModel, TaskModel


class CourseSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    #members = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True)

    class Meta:
        model = CourseModel
        #fields = '__all__'
        exclude = ('members',)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'