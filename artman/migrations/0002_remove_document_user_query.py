# Generated by Django 2.0.4 on 2018-04-20 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artman', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='user_query',
        ),
    ]
