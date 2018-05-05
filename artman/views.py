from django.shortcuts import render, redirect, get_object_or_404
from artman.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from artman.models import (
    BookShelf, Document, StudentGroup, PromoteRequest, get_full_data
)
from django.db.models import Q
from django.contrib.auth import authenticate, login
from artman.forms import SearchDocumentForm
from itertools import groupby, tee, chain
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homepage')

        return render(request, 'artman/index.html', {
            'user': request.user,
            'authform': AuthenticationForm(),
            })

    def post(self, request):
        if not request.user.is_authenticated:
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.warning(request, 'Неверное имя пользователя или пароль')
        return self.get(request)


class RegisterView(View):

    def get(self, request):
        creationform = UserCreationForm(request.POST)
        return render(request, 'artman/register.html', {
            'creationform': creationform
        })

    def post(self, request):
        if not request.user.is_authenticated:
            creationform = UserCreationForm(request.POST)
            if creationform.is_valid():
                UserModel = apps.get_model(settings.AUTH_USER_MODEL)
                data = {
                    'first_name': creationform.cleaned_data['first_name'],
                    'last_name': creationform.cleaned_data['last_name'],
                    'username': creationform.cleaned_data['username'],
                    'password': creationform.cleaned_data['password1'],
                }
                UserModel.objects.create_user(**data)
                user = authenticate(request, **data)
                if user is not None:
                    login(request, user)
                    return redirect('homepage')

        return self.get(request)


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        user_books = BookShelf.objects.filter(user=request.user).select_related()
        if user_books.exists():
            books = list(map(lambda x: x.article.pk, user_books))
            docs = Document.objects.exclude(pk__in=books)
        else:
            docs = Document.objects.all()

        sform = SearchDocumentForm(request.GET)
        if sform.is_valid():
            query = sform.cleaned_data.get('search')
            q = Q(title__contains=query)
            user_books = user_books.filter(article__title__contains=query)
            docs = docs.filter(q)

        return render(request, 'artman/homepage.html', {
            'sform': sform,
            'docs': docs,
            'bookshelf': user_books,
        })

    def post(self, request):
        art_id = request.POST.get('article', '-1')
        article = Document.objects.get(pk=art_id)
        add = request.POST.get('add', False)
        remove = request.POST.get('remove', False)
        check = BookShelf.objects.filter(user=request.user).filter(article=article)

        if add and not remove and not check.exists():
            BookShelf.objects.create(user=request.user, article=article)

        if remove and not add and check.exists():
            check.first().delete()

        return self.get(request)


class ModeratorView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        if request.user.is_superuser:
            init_filter = UserModel.objects.all()
        else:
            students = StudentGroup.objects.filter(prof=request.user).select_related()
            studs = map(lambda x: x.stud.pk, students)
            init_filter = UserModel.objects.filter(pk__in=studs)

        return render(request, 'artman/moderation.html', {
            'moderated': get_full_data(init_filter),
        })

    def post(self, request):
        apk = request.POST.get('article', '-1')
        article = get_object_or_404(Document, pk=apk)
        upk = request.POST.get('user', '-1')
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        user = get_object_or_404(UserModel, pk=upk)
        remove = request.POST.get('remove', False)
        add = request.POST.get('add', False)
        check = BookShelf.objects.filter(user=user).filter(article=article)

        if add and not remove and not check.exists():
            BookShelf.objects.create(user=user, article=article)

        if remove and not add and check.exists():
            check.first().delete()
        return self.get(request)


def promote_view(request):
    if not request.user.is_staff:
        if PromoteRequest.objects.filter(user=request.user).exists():
            messages.info(request, 'Ожидайте ответа')
        else:
            PromoteRequest.objects.get_or_create(user=request.user)
            messages.info(request, 'Запрос на модерацию был отправлен')
    return redirect('homepage')
