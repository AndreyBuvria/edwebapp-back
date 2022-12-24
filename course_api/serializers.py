from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CourseModel, TaskModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = CourseModel
        #fields = '__all__'
        exclude = ('members',)

