from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Photo,
    Comment
)

admin.site.register(User, UserAdmin)
admin.site.register(Photo)
admin.site.register(Comment)
