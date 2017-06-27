# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models

# Create your models here.
class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Country(DefaultModel):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class County(DefaultModel):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class CountryMap(DefaultModel):
    PROVICIAL='PR'
    COUNTY = 'CTY'
    CONSTITUENCY = 'CNY'
    PLAIN = 'PLN'

    BORDER_TYPE_CHOICES = (
        (PROVICIAL, 'Provincial'),
        (COUNTY, 'County'),
        (CONSTITUENCY, 'Constituency'),
        (PLAIN, 'Plain'),
    )

    border_type = models.CharField(
        max_length=3,
        choices=BORDER_TYPE_CHOICES,
        default=PLAIN,
    )
    country_represented = models.ForeignKey(Country)
    map_json = JSONField(default="")
    
    def __unicode__(self):
        return self.country_represented.name