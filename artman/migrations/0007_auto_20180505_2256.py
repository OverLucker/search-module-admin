# Generated by Django 2.0.4 on 2018-05-05 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artman', '0006_promoterequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='PupilsRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(blank=True, default=None, null=True)),
                ('result', models.CharField(choices=[('wait', 'ожидание'), ('accept', 'принято'), ('reject', 'отказано')], default='wait', max_length=6)),
                ('prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_proffessors', to=settings.AUTH_USER_MODEL)),
                ('stud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='diraccess',
            name='user',
        ),
        migrations.DeleteModel(
            name='DirAccess',
        ),
    ]
