from django.shortcuts import render
from django.views import generic
from .models import Photo


class ListAllPhotosView(generic.ListView):
    model = Photo
    template_name = 'app_pintagram/list_all_photos.html'
    context_object_name = 'list_of_all_photos'
