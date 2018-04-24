from django.shortcuts import render, redirect
from artman.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.conf import settings
from django.apps import apps
from django.contrib.auth.decorators import login_required, user_passes_test
from artman.models import BookShelf, Document
from django.db.models import Q
from django.contrib.auth import authenticate, login
from artman.forms import SearchDocumentForm


def index_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, 'artman/index.html', {
        'user': request.user,
        'creationform': CustomUserCreationForm(),
        'authform': CustomAuthenticationForm(),
    })


def authenticate_view(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
    return redirect('index_page')


def register_view(request):
    if request.method == 'POST' and not request.user.is_authenticated:
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
    if user_books.exists():
        # FIXME:
        books = list(map(lambda x: x.article.pk, user_books))
        docs = Document.objects.exclude(pk__in=books)
    else:
        docs = Document.objects.all()
    sform = SearchDocumentForm()
    if request.method == 'GET':
        sform = SearchDocumentForm(request.GET)
        if sform.is_valid():
            query = sform.cleaned_data.get('search')
            q = Q(title__contains=query)
            user_books = user_books.filter(article__title__contains=query)
            docs = docs.filter(q)

    if request.method == 'POST':
        art_id = request.POST.get('article', '-1')
        article = Document.objects.get(pk=art_id)
        add = request.POST.get('add', False)
        remove = request.POST.get('remove', False)
        check = BookShelf.objects.filter(user=request.user).filter(article=article)

        if add and not remove and not check.exists():
            BookShelf.objects.create(user=request.user, article=article)

        if remove and not add and check.exists():
            check.first().delete()

        return redirect('homepage')

    return render(request, 'artman/homepage.html', {
        'user': request.user,
        'sform': sform,
        'docs': docs,
        'bookshelf': user_books,
    })


@login_required
@user_passes_test(lambda user: user.is_staff)
def moderator_view(request):
    return redirect('homepage')
