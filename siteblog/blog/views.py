from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from .utils import *
from blog.forms import CreatePostForm, UpdatePostForm
from account.models import Account
import sweetify


# Class-based views

class Home(DataMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context(title="Главная")
        return context | context_mixin

    def get_queryset(self, cnt=3):
        return Post.objects.order_by('-created_at')[:cnt].prefetch_related('tags').select_related('category', 'author')


class AllPosts(DataMixin, ListView):
    model = Post
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context(title="Все посты")
        return context | context_mixin

    def get_queryset(self, cnt=3):
        return Post.objects.prefetch_related('tags', ).select_related('category', 'author').all()


class PostsByCategory(DataMixin, ListView):
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug']).prefetch_related('tags', ).select_related(
            'category', 'author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context(
            title="Посты в категории " + str(Category.objects.get(slug=self.kwargs['slug'])))
        return context | context_mixin


class PostsByTag(DataMixin, ListView):
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug']).prefetch_related('tags', ).select_related(
            'category', 'author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context(title="Посты по тегу " + str(Tag.objects.get(slug=self.kwargs['slug'])))
        return context | context_mixin


class GetPost(DataMixin, DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context | context_mixin


class Search(DataMixin, ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s')).prefetch_related('tags').select_related(
            'category', 'author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_user_context(title="Результат поиска", clear_req=self.request.GET.get('s'),
                                              s=f"s={self.request.GET.get('s')}&")
        return context | context_mixin


# Simple views


@login_required
def create_post_view(request):
    context = {}
    user = request.user

    form = CreatePostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        form.save_m2m()
        form = CreatePostForm()
        sweetify.success(request, 'Отлично!', text='Ваш пост был опубликован!',
                         persistent='OK', icon='success', confirmButtonColor='#f48840')

    if bool(form.errors):
        sweetify.success(request, 'Упс...', text='Исправьте ошибки и попробуйте заново',
                         persistent='OK', icon='error', confirmButtonColor='#f48840')

    context['create_form'] = form
    context['title'] = 'Создать публикацию'
    return render(request, 'blog/create_post.html', context)


@login_required()
def edit_post_view(request, slug):
    context = {}
    blog_post = get_object_or_404(Post, slug=slug)
    if request.POST:
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            tags_to_save = Tag.objects.filter(title__in=list(form.cleaned_data.get('tags')))
            obj.tags.set(tags_to_save)
            obj.save()
            blog_post = obj
            sweetify.success(request, 'Отлично!', text='Ваш пост был обновлен!',
                             persistent='OK', icon='success', confirmButtonColor='#f48840')

            if bool(form.errors):
                sweetify.success(request, 'Упс...', text='Исправьте ошибки и попробуйте заново',
                                 persistent='OK', icon='error', confirmButtonColor='#f48840')

    if blog_post.photo:
        form = UpdatePostForm(
            initial={
                "title": blog_post.title,
                "content": blog_post.content,
                "photo": blog_post.photo,
                "category": blog_post.category,
                "tags": blog_post.tags.all(),
            }
        )
    else:
        form = UpdatePostForm(
            initial={
                "title": blog_post.title,
                "content": blog_post.content,
                "category": blog_post.category,
                "tags": blog_post.tags.all(),
            }
        )

    context['form'] = form
    context['title'] = 'Изменить публикацию'
    context['post_title'] = blog_post.title
    return render(request, 'blog/edit_post.html', context)


def register(request):
    form = UserCreationForm()
    return render(request, 'blog/register.html', {"form": form})


def login(request):
    return render(request, 'blog/register.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def error_404(request, exception):
    return render(request, 'blog/404.html', {'title': 'Страница не найдена'})


def error_500(request):
    return render(request, 'blog/404.html', {'title': 'Ошибка сервера'})
