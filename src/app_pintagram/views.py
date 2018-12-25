from django.shortcuts import (
    render,
    reverse
)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import generic
from django.conf import settings
from .models import Post
from .forms import (
    PostForm,
    CommentForm,
    SignInForm,
    UpdateCustomUserForm,
)


class ListAllPostsView(generic.ListView):
    model               = Post
    template_name       = 'app_pintagram/list_all_posts.html'
    context_object_name = 'list_of_all_posts'
    ordering            = ['-creation_datetime']


class SignInView(generic.CreateView):
    model         = get_user_model()
    template_name = 'app_pintagram/sign_in.html'
    form_class    = SignInForm
    success_url   = reverse_lazy('login')

    def form_valid(self, form):
        rsp = super().form_valid(form)
        messages.success(self.request, 'Account successfully created!')
        return rsp


class CustomUserDetailView(generic.DetailView):
    model               = get_user_model()
    template_name       = 'app_pintagram/user_details.html'
    context_object_name = 'user_details'


class UpdateCustomUserView(generic.UpdateView):
    model         = get_user_model()
    template_name = 'app_pintagram/user_update.html'
    fields        = ['username', 'first_name', 'last_name', 'email', 'profile_photo']

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        rsp = super().form_valid(form)
        messages.success(self.request, 'User information successfully updated!')
        return rsp


class DeleteCustomUser(generic.DeleteView):
    model         = get_user_model()
    template_name = 'app_pintagram/user_delete.html'
    success_url   = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        deleted_user = self.get_object()
        rsp          = super().post(request, *args, **kwargs)
        messages.warning(self.request, f'User {deleted_user.username} has been successfully deleted.')
        return rsp


class CreatePostView(generic.CreateView):
    model         = Post
    template_name = 'app_pintagram/post_create.html'
    form_class    = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        rsp                  = super().form_valid(form)
        messages.success(self.request, 'Post successfully created!')
        return rsp

    def form_invalid(self, form):
        rsp = super().form_invalid(form)
        messages.error(self.request, 'Form wasn\'t filled correctly.')
        return rsp


class PostDetailsView(generic.DetailView):
    model         = Post
    template_name = 'app_pintagram/post_details.html'


class UpdatePostView(generic.UpdateView):
    model         = Post
    template_name = 'app_pintagram/post_update.html'
    fields        = ['description']

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        rsp = super().form_valid(form)
        messages.success(self.request, 'Post successfully updated!')
        return rsp


class DeletePostView(generic.DeleteView):
    model         = Post
    template_name = 'app_pintagram/post_delete.html'
    success_url   = reverse_lazy('list-of-all-posts')

    def post(self, request, *args, **kwargs):
        rsp          = super().post(request, *args, **kwargs)
        messages.warning(self.request, f'Post has been successfully deleted.')
        return rsp
