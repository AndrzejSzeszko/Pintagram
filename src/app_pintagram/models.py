from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_pics', default='dafault_user.jpg')
