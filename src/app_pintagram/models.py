from django.contrib.auth import (
    models as auth_models,
    get_user_model
)
from django.shortcuts import reverse
from django.db import models
from django.conf import settings
from PIL import Image


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Deleted_user')[0]


class CustomUser(auth_models.AbstractUser):
    email         = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_pics', default='default_user.jpg')
    is_blocked    = models.BooleanField(default=False)
    likes_posts   = models.ManyToManyField('Post', through='PostLike', related_name='liked_by')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_photo.path)
        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)

    def __str__(self):
        return self.username


class Post(models.Model):
    author            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo             = models.ImageField(upload_to='posted_photos')
    # path              = models.FilePathField()
    description       = models.TextField(max_length=256, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    # thumbs_up         = models.PositiveIntegerField(default=0)
    # thumbs_down       = models.PositiveIntegerField(default=0)
    is_blocked        = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': self.pk})

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.photo.path)
        if img.width > 400 or img.height > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return f'Post of id {self.id} by {self.author}'


class Comment(models.Model):
    author            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    post              = models.ForeignKey(Post, on_delete=models.CASCADE)
    content           = models.TextField(max_length=256)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_blocked        = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment of id {self.id} by {self.author} on Post of id {self.post_id}'


class PostLike(models.Model):
    user              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    post              = models.ForeignKey(Post, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.post}'

    @property
    def slug(self):
        return f'p{self.post.pk}u{self.user.pk}'

    class Meta:
        unique_together = ['user', 'post']
