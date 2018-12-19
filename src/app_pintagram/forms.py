#!/usr/bin/python3.7


from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    model = Photo
    fields = '__all__'
