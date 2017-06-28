# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 14:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0003_auto_20170627_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countrymap',
            old_name='geojson',
            new_name='map_json',
        ),
        migrations.RemoveField(
            model_name='countrymap',
            name='topojson',
        ),
    ]