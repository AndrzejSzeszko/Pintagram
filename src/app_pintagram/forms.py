#!/usr/bin/python3.7
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Photo,
    Comment
)


class SignInForm(UserCreationForm):
    class Meta:
        model  = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class PhotoForm(forms.ModelForm):
    class Meta:
        model  = Photo
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['content']
