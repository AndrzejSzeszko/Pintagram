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


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    form = UpdateCustomUserForm


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
