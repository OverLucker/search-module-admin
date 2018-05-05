"""file_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from artman.views import (
    LoginView, RegisterView, HomeView, ModeratorView, PupilRequestView,
    StudentsView, promote_view
)
from django.contrib.auth import views as authviews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(next_page='logout_success'), name='logout'),
    path('bye/', TemplateView.as_view(template_name='artman/bye.html'), name='logout_success'),
    path('moderate/', ModeratorView.as_view(), name='moderate_page'),
    path('promote/', promote_view, name='promote_request'),
    path('instructors/', PupilRequestView.as_view(), name='pupilrequest_page'),
    path('students/', StudentsView.as_view(), name='studentsrequest_page'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
