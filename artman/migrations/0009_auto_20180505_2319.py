# Generated by Django 2.0.4 on 2018-05-05 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artman', '0008_auto_20180505_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promoterequest',
            name='user',
        ),
        migrations.DeleteModel(
            name='PromoteRequest',
        ),
    ]
