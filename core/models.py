from django.contrib.auth.models import AbstractUser
from django.db import models

from course_api.models import CourseModel


# Create your models here.
class UserProfile(AbstractUser):
    STUDENT = 0
    TEACHER = 1
    USER_LEVEL_CHOICES = (
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
    )
    firstname = models.CharField(max_length=36)
    lastname = models.CharField(max_length=40)
    email = models.EmailField()
    role = models.IntegerField(choices=USER_LEVEL_CHOICES, default=STUDENT)
    about       = models.TextField()
    timecreate  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timecreate',)
