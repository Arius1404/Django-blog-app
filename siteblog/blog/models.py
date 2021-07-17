from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from ckeditor.fields import RichTextField
from unidecode import unidecode
from django.template import defaultfilters


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, verbose_name='URL тега', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название публикации', null=False, blank=False)
    slug = models.SlugField(max_length=255, verbose_name='URL поста', unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    content = RichTextField(blank=True, verbose_name='Содержание', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее редактирование')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts',
                                 verbose_name='Категория публикации')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Теги')
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация(ю)'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.photo.delete(False)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = defaultfilters.slugify(unidecode(instance.title))


pre_save.connect(pre_save_post_receiver, sender=Post)
