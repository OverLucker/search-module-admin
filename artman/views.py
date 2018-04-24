from django.shortcuts import render, redirect
from artman.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.conf import settings
from django.apps import apps
from django.contrib.auth.decorators import login_required
from artman.models import BookShelf, Document
from django.db.models import Q


def index_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, 'artman/index.html', {
        'creationform': CustomUserCreationForm(),
        'authform': CustomAuthenticationForm(),
    })


def register_view(request):
    if request.method == 'POST':
        creationform = CustomUserCreationForm(request.POST)
        if creationform.is_valid():
            UserModel = apps.get_model(settings.AUTH_USER_MODEL)
            data = {
                'username': creationform.cleaned_data['username'],
                'password': creationform.cleaned_data['password1'],
            }
            UserModel.objects.create_user(**data)

        return render(request, 'artman/index.html', {
            'creationform': creationform,
            'authform': CustomAuthenticationForm(request.POST)
        })

    return redirect('index_page')


@login_required
def home_view(request):
    user_books = BookShelf.objects.filter(user=request.user)
    docs = Document.objects.filter(pk__in=user_books)
    if request.method == 'GET':
        query = request.GET.get('q', None)
        if query:
            q = Q(title__contains=query)
            user_books = user_books.filter(article__title__contains=query)
            docs = docs.filter(q)

    return render(request, 'artman/homepage.html', {
        'user': request.user,
        'docs': docs,
        'bookshelf': user_books,
    })
