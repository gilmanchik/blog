from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import *


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    posts = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post_detail.html', {'posts': posts})
