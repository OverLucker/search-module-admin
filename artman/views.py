from django.shortcuts import render, redirect
from artman.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.conf import settings
from django.apps import apps


def index_view(request):
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


def auth_view(request):
    if request.method == 'POST':
        authform = CustomAuthenticationForm(request.POST)
        if authform.is_valid():
            UserModel = settings.AUTH_USER_MODEL
            UserModel.create_user(**authform.cleaned_data)


def home_view(request):
    return render(request, 'artman/homepage.html', {
        'user': request.user
    })
