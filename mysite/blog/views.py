from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import *
from .models import *


def post_list(request, tag_slug=None):
    post = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    paginator = Paginator(post, 3)
    page_number = request.GET.get('page', 1)
    try:
        post = paginator.page(page_number)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        post = paginator.page(1)
    return render(request,
                  'blog/post_list.html',
                  {'post': post, 'tag': tag})


# class PostList(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'post'
#     template_name = 'blog/post_list'
#     paginate_by = 3


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=False)
    simular_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    simular_post = simular_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'form': form,
                                                     'comments': comments,
                                                     'simular_post': simular_post})


def post_share(request, post_id):
    posts = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(posts.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {posts.title}'
            message = f'read {posts.title} at {post_url}\n\n' \
                      f'{cd["name"]} comments to {cd["comments"]}'
            send_mail(subject, message, 'gilman9189@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post_share.html',
                  {'posts': posts, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post_comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gte=0.1).order_by('-similarity')

    return render(request, 'blog/post_search.html', {
        'form': form,
        'query': query,
        'results': results
    })
