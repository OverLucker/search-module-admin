from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class UserQueryManager(models.Manager):
    def all(self):
        return self.order_by('-id')


class UserQuery(models.Model):
    class Meta:
        ordering = ['-id']
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    keywords = models.CharField(max_length=255, default="")
    year1 = models.CharField(max_length=4, default="")
    year2 = models.CharField(max_length=4, default="")
    # finish = models.BooleanField(default=False)
    # objects = UserQueryManager()

    def get_url(self):
        return "/query_detail/{}/".format(self.timestamp)

    def get_absolute_url(self):
        return reverse('query_detail', kwargs={'timestamp': self.timestamp})

    def __str__(self):
        return self.timestamp


def upload_path(ins, filename):
    return filename


class Document(models.Model):
    # user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_path,
        max_length=600
    )
    net_url = models.URLField(max_length=600)
    title = models.CharField(max_length=200)
    #query_url = models.URLField()

    # @models.permalink
    # def get_absolute_url(self):
    #     return str(self.local_url)

    def __str__(self):
        return self.title

class BaseUrlParser(models.Model):
    user_query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    url_cyberleninka = models.URLField(max_length=600)
    url_scholar = models.URLField(max_length=600)
    url_socio = models.URLField(max_length=600)

    def __str__(self):
        return 'Base url #' + str(self.id)
