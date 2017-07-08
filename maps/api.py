from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from django.http import HttpResponse, JsonResponse
from analysis import counties, constituencies
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

class KenyaCountyList(generics.ListAPIView):
    def get(self, request):
        result = counties.get_county_codes()

        return HttpResponse(result)


class CountyConstituencyList(generics.ListAPIView):
    def get(self, request, **kwargs):
        result = constituencies.get_county_constituency_codes_json(kwargs['county_id'])
        # result = 'consituency list'
        return HttpResponse(result)
