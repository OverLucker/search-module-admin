# Generated by Django 2.0.4 on 2018-04-23 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artman', '0003_auto_20180423_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='local_url',
            new_name='file',
        ),
    ]
