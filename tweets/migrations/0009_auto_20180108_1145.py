# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 11:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_tweets_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]