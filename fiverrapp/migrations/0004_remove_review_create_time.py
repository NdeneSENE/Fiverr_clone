# Generated by Django 2.2.1 on 2019-05-23 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fiverrapp', '0003_review_create_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='create_time',
        ),
    ]
