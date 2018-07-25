# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 13:55
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrymap',
            name='country_represented',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maps.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='countrymap',
            name='geojson',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
            preserve_default=False,
        ),
    ]
