from django.shortcuts import (
    render,
    reverse
)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import generic
from django.conf import settings
from .models import Photo
from .forms import (
    PhotoForm,
    CommentForm,
    SignInForm
)


class ListAllPhotosView(generic.ListView):
    model               = Photo
    template_name       = 'app_pintagram/list_all_photos.html'
    context_object_name = 'list_of_all_photos'


class SignInView(generic.CreateView):
    model         = get_user_model()
    template_name = 'app_pintagram/sign_in.html'
    form_class    = SignInForm
    success_url   = reverse_lazy('login')
