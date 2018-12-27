#!/usr/bin/python3.7
from django import template


def likes_count(post_obj):
    return post_obj.liked_by.all().count()


def comments_count(post_obj):
    return post_obj.comment_set.all().count()


register = template.Library()

register.filter('likes_count', likes_count)
register.filter('comments_count', comments_count)
