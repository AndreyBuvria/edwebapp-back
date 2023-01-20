import random
import string

from django.contrib.auth import get_user_model
from django.db import models

from edappback import settings
from .constants import model_setting

# Create your models here.

def key_generator(size=model_setting['KEY_SIZE'], chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class CourseModel(models.Model):
    PUBLIC = 0
    ACCESS = 1
    ACCESS_CHOICES = (
        (PUBLIC, "Public"),
        (ACCESS, "Private"),
    )

    key = models.CharField(max_length=model_setting['KEY_SIZE'], editable=False, default=key_generator())
    name = models.CharField(max_length=36)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access = models.IntegerField(choices=ACCESS_CHOICES, default=PUBLIC)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
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
    expires = models.DateTimeField(null=True)

    def __str__(self):
        return self.name