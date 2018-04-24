from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from artman.models import BookShelf


class CustomAuthenticationForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    prefix = 'creationform'


class SearchDocumentForm(forms.Form):
    search = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control mr-sm-2',
            'placeholder': 'Найти',
            'type': 'search',
            'aria-label': 'Найти',
            'name': 'q'
        })
    )
