#!/usr/bin/python3.7
from django import forms
from .models import (
    Photo,
    Comment
)


class PhotoForm(forms.ModelForm):
    model = Photo
    fields = '__all__'


class CommentForm(forms.ModelForm):
    model = Comment
    fields = ['content']
