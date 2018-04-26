from django.contrib import admin
from artman.models import BookShelf, StudentGroup
from artman.models_anton import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'taccess')
    readonly_fields = ('taccess', )

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs).filter(user__is_staff=True)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('prof', 'stud', 'start')
    readonly_fields = ('start', )
