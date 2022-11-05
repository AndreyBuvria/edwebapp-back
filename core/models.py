from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Role(models.Model):
    name    = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    role        = models.ForeignKey(Role, on_delete=models.CASCADE)
    about       = models.TextField()
    timecreate  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timecreate',)