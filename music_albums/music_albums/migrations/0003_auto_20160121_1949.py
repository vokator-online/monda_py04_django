# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-22 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_albums', '0002_auto_20160121_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], verbose_name='Rating'),
        ),
    ]