# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-29 05:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20171228_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tweets.Tweets'),
        ),
    ]
