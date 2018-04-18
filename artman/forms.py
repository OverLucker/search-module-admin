from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomAuthenticationForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    prefix = 'creationform'
