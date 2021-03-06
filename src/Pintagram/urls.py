"""Pintagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app_pintagram import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ListAllPostsView.as_view(), name='list-of-all-posts'),
    path('login/', auth_views.LoginView.as_view(template_name='app_pintagram/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app_pintagram/logout.html'), name='logout'),
    path('sign_up/', views.SignUpView.as_view(), name='sign-up'),
    path('user/details/<int:pk>/', views.CustomUserDetailView.as_view(), name='user-details'),
    path('user/update/<int:pk>/', views.UpdateCustomUserView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', views.DeleteCustomUser.as_view(), name='user-delete'),
    path('post/create/', views.CreatePostView.as_view(), name='post-create'),
    path('post/details/<int:pk>/', views.PostDetailsView.as_view(), name='post-details'),
    path('post/update/<int:pk>/', views.UpdatePostView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', views.DeletePostView.as_view(), name='post-delete'),
    path('comment/delete/<int:pk>/', views.DeleteCommentView.as_view(), name='comment-delete'),
    # path('post_like/create/', views.PostLikeCreateView.as_view(), name='post-like-create'),
    # path('post_like/destroy/<int:post_id>/', views.PostLikeDestroyView.as_view(), name='post-like-destroy'),
    # path('post_like/', views.PostLikeView.as_view(), name='post-like'),
    path('post_like/', views.PostLikeView.as_view(), name='post-like'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
