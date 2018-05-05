from django.db import models
from django.conf import settings
from django.utils import timezone
# FIXME: set Document
from artman.models_anton import Document


def get_full_data(user_set):

    for user in user_set.order_by('username'):
        docs = BookShelf.objects.filter(user=user).select_related()
        books_pk = map(lambda x: x.article.pk, docs)
        adocs = Document.objects.exclude(pk__in=list(books_pk))
        yield user, docs, adocs


class DirAccess(models.Model):
    class Meta:
        verbose_name = "Доступ к директории"
        verbose_name_plural = "Доступ к директории"

    PERMISSION_CHOICES = (
        (1, "чтение"),
        (2, "запись"),
        (3, "чтение и запись"),
        (4, "удаление"),
        (7, "чтение, запись и удаление"),
    )

    dirname = models.CharField(max_length=25)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    permissions = models.IntegerField(choices=PERMISSION_CHOICES)


class BookShelf(models.Model):
    # class Meta:
    #     verbose_name =

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    article = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )

    taccess = models.DateTimeField(default=timezone.now)


class StudentGroup(models.Model):
    prof = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proffessors'
    )

    stud = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='students'
    )

    start = models.DateTimeField(
        default=timezone.now
    )


class PromoteRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
