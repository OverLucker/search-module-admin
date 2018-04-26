from django import forms
from artman.models import BookShelf


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'имя пользователя',
            })
    )

    password = forms.CharField(max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'пароль',
            })
    )


class UserCreationForm(forms.Form):
    prefix = 'creationform'
    username = forms.CharField(max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'имя пользователя',
            })
    )

    password1 = forms.CharField(max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'пароль',
            })
    )

    password2 = forms.CharField(max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'пароль повторить',
            })
    )


class SearchDocumentForm(forms.Form):
    search = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control w-50 mr-2',
            'placeholder': 'Найти',
            'type': 'search',
            'aria-label': 'Найти',
            'name': 'q',
            'style': 'min-width: 50%;'
        })
    )
