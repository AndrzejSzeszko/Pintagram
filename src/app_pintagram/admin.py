from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import (
    Photo,
    Comment
)


class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = get_user_model()


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Photo)
admin.site.register(Comment)
