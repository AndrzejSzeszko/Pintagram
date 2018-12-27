from django.shortcuts import (
    render,
    reverse,
    redirect
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostLikeSerializer
from django.db.models import F
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import (
    Post,
    Comment,
    PostLike,
)
from .forms import (
    PostForm,
    CommentForm,
    SignInForm,
    UpdateCustomUserForm,
)


class ListAllPostsView(LoginRequiredMixin, generic.ListView):
    model               = Post
    template_name       = 'app_pintagram/list_all_posts.html'
    context_object_name = 'list_of_all_posts'
    ordering            = ['-creation_datetime']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)


class SignInView(generic.CreateView):
    model         = get_user_model()
    template_name = 'app_pintagram/sign_in.html'
    form_class    = SignInForm
    success_url   = reverse_lazy('login')

    def form_valid(self, form):
        rsp = super().form_valid(form)
        messages.success(self.request, 'Account successfully created!')
        return rsp


class CustomUserDetailView(LoginRequiredMixin, generic.DetailView):
    model               = get_user_model()
    template_name       = 'app_pintagram/user_details.html'
    context_object_name = 'user_details'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'user_details_posts': self.get_object().post_set.filter(is_blocked=False)})
        return ctx


class UpdateCustomUserView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model         = get_user_model()
    template_name = 'app_pintagram/user_update.html'
    fields        = ['username', 'first_name', 'last_name', 'email', 'profile_photo']

    def get_queryset(self):
        return self.model.objects.filter(is_blocked=False)

    def get_success_url(self):
        return reverse_lazy('user-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        rsp = super().form_valid(form)
        messages.success(self.request, 'User information successfully updated!')
        return rsp

    def test_func(self):
        return self.get_object() == self.request.user


class DeleteCustomUser(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model         = get_user_model()
    template_name = 'app_pintagram/user_delete.html'
    success_url   = reverse_lazy('login')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def post(self, request, *args, **kwargs):
        deleted_user = self.get_object()
        rsp          = super().post(request, *args, **kwargs)
        messages.warning(self.request, f'User {deleted_user.username} has been successfully deleted.')
        return rsp

    def test_func(self):
        return self.get_object() == self.request.user


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model         = Post
    template_name = 'app_pintagram/post_create.html'
    form_class    = PostForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def form_valid(self, form):
        form.instance.author = self.request.user
        rsp                  = super().form_valid(form)
        messages.success(self.request, 'Post successfully created!')
        return rsp

    def form_invalid(self, form):
        messages.error(self.request, 'Form wasn\'t filled correctly.')
        return super().form_invalid(form)


class PostDetailsView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model         = Post
    template_name = 'app_pintagram/post_details.html'
    form_class    = CommentForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                'comments': Comment.objects.filter(post=self.object, is_blocked=False),
                'likes': PostLike.objects.filter(post=self.object).count(),
                'is_post_liked': True if self.object.liked_by.filter(pk=self.request.user.pk) else False
            }
        )
        return ctx

    def get_redirect_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, *args, **kwargs):
        form                 = self.get_form()
        form.instance.author = self.request.user
        form.instance.post   = self.get_object()
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Comment successfully posted!')
        else:
            messages.error(self.request, 'Comment content was filled improperly.')
        return redirect(self.get_redirect_url())


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model         = Post
    template_name = 'app_pintagram/post_update.html'
    fields        = ['description']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        messages.success(self.request, 'Post successfully updated!')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model         = Post
    template_name = 'app_pintagram/post_delete.html'
    success_url   = reverse_lazy('list-of-all-posts')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def post(self, request, *args, **kwargs):
        messages.warning(self.request, 'Post has been successfully deleted.')
        return super().post(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model         = Comment
    template_name = 'app_pintagram/comment_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.get_object().post.pk})

    def post(self, request, *args, **kwargs):
        messages.warning(self.request, f'{self.get_object()} has been successfully deleted.')
        return super().post(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user


class PostLikeView(generic.View): #  todo działa ale zrobić przez serializator tak aby można było po bożemu użyc metod POST i DELETE

    def get(self, request):
        post_id  = request.GET.get('post_id')
        like_or_unlike = request.GET.get('like_or_unlike')
        if like_or_unlike == 'like':
            PostLike.objects.create(
                post=Post.objects.get(pk=post_id),
                user=get_user_model().objects.get(pk=request.user.id)
            )
            return JsonResponse(True, safe=False)
        else:
            PostLike.objects.filter(
                post=Post.objects.get(pk=post_id),
                user=get_user_model().objects.get(pk=request.user.id)
            ).delete()
            return JsonResponse(False, safe=False)

#
# class PostLikeView(APIView):
#
#     def post(self, request):
#         data = request.data
#         data['user'] = request.user
#         serializer = PostLikeSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         pass
#
#
#
# class PostLikeDestroyView(DestroyAPIView):
#     pass
