from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    prefix = 'creationform'


class SearchDocumentForm(forms.Form):
    pass
