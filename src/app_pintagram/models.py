from django.contrib.auth import (
    models as auth_models,
    get_user_model
)
from django.db import models
from django.conf import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Deleted_user')[0]


class User(auth_models.AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_pics', default='default_user.jpg')


class Photo(models.Model):
    author            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path              = models.FilePathField()
    description       = models.TextField(max_length=256, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    thumbs_up         = models.PositiveIntegerField(default=0)
    thumbs_down       = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    author            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    photo             = models.ForeignKey(Photo, on_delete=models.CASCADE)
    content           = models.TextField(max_length=256)
    creation_datetime = models.DateTimeField(auto_now_add=True)

