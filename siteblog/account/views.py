from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
import sweetify
from blog.models import Post


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
        context['title'] = "Регистрация :: Ilya's Blog"
    return render(request, 'blog/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    context['title'] = "Вход в аккаунт :: Ilya's Blog"
    return render(request, 'blog/login.html', context)


@login_required
def account_view(request):
    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Отлично!', text='Изменения были применены',
                             persistent='OK', icon='success', confirmButtonColor='#f48840')
        if bool(form.errors):
            sweetify.success(request, 'Упс...', text='Исправьте ошибки и попробуйте заново',
                             persistent='OK', icon='error', confirmButtonColor='#f48840')
    else:
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
            }
        )

    context['account_form'] = form
    context['title'] = 'Редактирование аккаунта'

    blog_posts = Post.objects.filter(author=request.user).select_related('category', 'author').prefetch_related('tags')
    context['blog_posts'] = blog_posts

    return render(request, 'blog/account.html', context)
