from rest_framework import serializers
from django.db import transaction
from models import *


#start of inline serializers
class CountryInlineSerializer(serializers.ModelSerializer):
    country_maps = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Country
        fields = ( 'name','country_maps')

class CountryMapInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMap
        fields = '__all__'