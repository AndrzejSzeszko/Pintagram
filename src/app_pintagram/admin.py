from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import (
    Post,
    Comment
)
from .forms import (
    UpdateCustomUserForm,
    SignInForm
)


def block_object(model_admin, request, queryset):
    queryset.update(is_blocked=True)


block_object.short_description = 'Block selected objects'


def unblock_object(model_admin, request, queryset):
    queryset.update(is_blocked=False)


unblock_object.short_description = 'Unblock selected objects'


def description_abstract(post_obj):
    return f'{post_obj.description[:10]}...'


def content_abstract(comment_obj):
    return f'{comment_obj.content[:10]}...'


def post_likes_count(post_obj):
    return post_obj.liked_by.all().count()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_blocked',
    ]
    form = UpdateCustomUserForm
    actions = [
        block_object,
        unblock_object,
    ]


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        'photo',
        description_abstract,
        'creation_datetime',
        post_likes_count,
        'is_blocked',
    ]
    actions = [
        block_object,
        unblock_object,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        'post',
        content_abstract,
        'creation_datetime',
        'is_blocked',
    ]
    actions = [
        block_object,
        unblock_object,
    ]


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
