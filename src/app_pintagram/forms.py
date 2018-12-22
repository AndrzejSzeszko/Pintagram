#!/usr/bin/python3.7
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
)
from .models import (
    Post,
    Comment
)


class SignInForm(UserCreationForm):
    class Meta:
        model  = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UpdateCustomUserForm(UserChangeForm):
    class Meta:
        model  = get_user_model()
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['photo', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['content']
