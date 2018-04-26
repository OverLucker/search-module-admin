# Generated by Django 2.0.4 on 2018-04-24 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artman', '0004_auto_20180423_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('prof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proffessors', to=settings.AUTH_USER_MODEL)),
                ('stud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='userquery',
            options={'ordering': ['-id']},
        ),
    ]