from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth_user.serializers import UserReadSerializer

from .models import CourseModel, TaskModel
from .constants import model_setting


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    members = UserReadSerializer(many=True)
    access = ChoiceField(choices=CourseModel.ACCESS_CHOICES)

    class Meta:
        model = CourseModel
        fields = '__all__'
        #exclude = ('members',)

class CourseAddSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=model_setting['KEY_SIZE'])

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    