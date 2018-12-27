# !/usr/bin/python3.7
from rest_framework import serializers
from .models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=PostLike.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=PostLike.objects.all())

    class Meta:
        model  = PostLike
        fields = '__all__'
