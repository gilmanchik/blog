from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'PUBLISHED'

    title = models.CharField(
        max_length=32,
        verbose_name='Заголовок'
    )

    slug = models.SlugField(
        max_length=32,
        verbose_name='Слаг'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    body = models.TextField(
        verbose_name='Текст'
    )

    publish = models.DateTimeField(
        default=timezone.now
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    updated = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        max_length=2,
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
