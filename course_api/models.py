from django.contrib.auth import get_user_model
from django.db import models

from edappback import settings

# Create your models here.

class CourseModel(models.Model):
    name = models.CharField(max_length=36)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members', blank=True)
    description = models.TextField()
    timecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name;

    class Meta:
        managed = True
        verbose_name = 'CourseModel'
        verbose_name_plural = 'CourseModels'

class TaskModel(models.Model):
    related_course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=36)
    description = models.TextField()
    timecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
