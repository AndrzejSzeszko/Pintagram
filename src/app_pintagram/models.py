from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_pics', default='dafault_user.jpg')


class Photo(models.Model):
    author            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path              = models.FilePathField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    thumbs_up         = models.PositiveIntegerField(default=0)
    thumbs_down       = models.PositiveIntegerField(default=0)
