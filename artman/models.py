from django.db import models
from django.conf import settings
from django.utils import timezone
# FIXME: set Document
from artman.models_anton import Document


def get_prof_data(user_set):
    for user in user_set.order_by('username'):
        docs = BookShelf.objects.filter(user=user).select_related()
        books_pk = map(lambda x: x.article.pk, docs)
        adocs = Document.objects.exclude(pk__in=list(books_pk))
        yield user, docs, adocs


def get_stud_data(user_set):
    for user in user_set.order_by('username'):
        docs = BookShelf.objects.filter(user=user).select_related()
        books_pk = map(lambda x: x.article.pk, docs)
        adocs = Document.objects.exclude(pk__in=list(books_pk))
        yield user, docs, adocs


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
    class Meta:
        app_label = 'auth'
        verbose_name = 'запрос на повышение'
        verbose_name_plural = 'запросы на повышение'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class PupilsRequest(models.Model):
    STATUS_CHOICES = (
        ('wait', 'ожидание'),
        ('accept', 'принято'),
        ('reject', 'отказано'),
    )
    prof = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='request_proffessors'
    )

    stud = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='request_students'
    )

    start = models.DateTimeField(
        default=timezone.now
    )

    end = models.DateTimeField(
        blank=True,
        null=True,
        default=None
    )

    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )
