# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-28 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import tweets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20171225_0729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweets',
            options={'ordering': ['-timestamp', 'content']},
        ),
        migrations.AlterField(
            model_name='tweets',
            name='content',
            field=models.CharField(max_length=140, validators=[tweets.validators.validate_content]),
        ),
    ]