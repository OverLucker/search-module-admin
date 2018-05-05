from django.contrib import admin
from artman.models import BookShelf, StudentGroup, PromoteRequest
from artman.models_anton import Document
from django.utils.html import mark_safe
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.apps import apps


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'taccess')
    readonly_fields = ('taccess', )

    def get_queryset(self, request):
        UserModel = apps.get_model(settings.AUTH_USER_MODEL)
        if request.user.is_superuser:
            init_filter = UserModel.objects.all()
        else:
            students = StudentGroup.objects.filter(prof=request.user).select_related()
            studs = map(lambda x: x.stud.pk, students)
            init_filter = UserModel.objects.filter(pk__in=studs)
        return super().get_queryset(request).filter(user__in=init_filter)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('prof', 'stud', 'start')
    readonly_fields = ('start', )


@admin.register(PromoteRequest)
class PromoteRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'promote')

    def promote(self, obj):
        url = reverse('admin:%s_%s_promote-user' % (obj._meta.app_label,  obj._meta.model_name),  args=[obj.pk] )
        return mark_safe('<a href="{}">удовлетворить</a>'.format(url))
    promote.short_description = "удовлетворить"

    def get_urls(self):
        print('gettings urls')
        from django.urls import path
        default = super().get_urls()
        custom = [
            path(r'<str:obj_id>/promote',
            self.admin_site.admin_view(self.promote_view),
            name='{}_{}_promote-user'.format(self.model._meta.app_label, self.model._meta.model_name))
        ]
        print(default + custom)
        return default + custom

    def promote_view(self, request, obj_id):
        obj = self.get_object(request, obj_id)
        if obj and not obj.user.is_staff:
            obj.user.is_staff = True
            obj.user.save()
            obj.delete()
            messages.info(request, 'User {} promoted'.format(obj.user))
        return redirect('admin:%s_%s_changelist' % (obj._meta.app_label,  obj._meta.model_name))
