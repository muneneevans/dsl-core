from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from django.http import HttpResponse, JsonResponse
from analysis import counties, constituencies, wards
from .serializers import *
from .models import *

# import maps_data_analysis

class CountryListView(generics.ListAPIView):
    model = Country

    queryset = Country.objects.all()
    serializer_class = CountryInlineSerializer

class CountryPlainMapView(generics.RetrieveAPIView):
    models = CountryMap
    queryset = CountryMap.objects.all()
    serializer_class = CountryMapInlineSerializer
    lookup_field = 'country_represented'

# class KenyaCountyMapView(generics.ListAPIView):
#     def get(self, request):
#         result = maps_data_analysis.get_kenya_county_map()

        # return JsonResponse(result)

class KenyaCountyList(generics.ListAPIView):
    def get(self, request):
        result = counties.get_county_codes()

        return HttpResponse(result)

class CountyConstituencyList(generics.ListAPIView):
    def get(self, request, **kwargs):
        result = constituencies.get_county_constituency_codes(kwargs['county_id'], True)
        # result = 'consituency list'
        return HttpResponse(result)

class ConstituencyWardList(generics.ListAPIView):
    def get(self, request, **kwargs):
        result = wards.get_constituency_wards(kwargs['constituency_id'], True)

        return HttpResponse(result)

class WardDetails(generics.ListAPIView):
    def get(self, request, **kwargs):
        response = wards.get_ward_by_id(kwargs['ward_id'], True)
        return HttpResponse(response)