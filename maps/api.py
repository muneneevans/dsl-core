from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from django.http import HttpResponse, JsonResponse

from .serializers import *
from .models import *

import maps_data_analysis

class CountryListView(generics.ListAPIView):
    model = Country

    queryset = Country.objects.all()
    serializer_class = CountryInlineSerializer

class CountryPlainMapView(generics.RetrieveAPIView):
    models = CountryMap
    queryset = CountryMap.objects.all()
    serializer_class = CountryMapInlineSerializer
    lookup_field = 'country_represented'

class KenyaCountyMapView(generics.ListAPIView):
    def get(self, request):
        result = maps_data_analysis.get_kenya_county_map()

        return JsonResponse(result)
