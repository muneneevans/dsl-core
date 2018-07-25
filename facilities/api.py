from rest_framework import generics
from rest_framework.generics import ListAPIView
from analysis import facilities
from django.http import HttpResponse, JsonResponse
import json

class FacilityDetails(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_facility_by_id(kwargs['facility_id'], True)
        return HttpResponse(response)
    
class FaciltyTypeListView(ListAPIView):
    def get(self, request ):
        result = facilities.get_facility_types_codes(True)
        return HttpResponse(result)

class FacilityKephLevelsView(ListAPIView):
    def get(self, request):
        result = facilities.get_facility_keph_levels_codes(True)
        return HttpResponse(result)
    
class CountrySummary(ListAPIView):
    def get(self, request):
        response = facilities.get_country_summary(True)
        return HttpResponse(response)

class CountryFacilityTypeSummary(ListAPIView):
    def get(self, request):
        response  = facilities.get_country_facility_type_summary(True)
        return HttpResponse(response)
class CountryKephLevelsSummary(ListAPIView):
    def get(self, request):
        response  = facilities.get_country_keph_level_summary(True)
        return HttpResponse(response)

class CountryBedsSummary(ListAPIView):
    def get(self, request):
        response = facilities.get_country_beds_summary(True)
        return HttpResponse(response)
class CountyFacilities(ListAPIView):
    def get(self, request, **kwargs):
        result = facilities.get_county_facilities(kwargs['county_id'],True)
        return HttpResponse(result)

class CountySummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_county_summary(kwargs['county_id'], True)
        return HttpResponse(response)

class CountyFacilityTypesSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_county_facility_type_summary(kwargs['county_id'], True)
        return HttpResponse(response)

class CountyKephLevelsSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_county_keph_level_summary(kwargs['county_id'], True)
        return HttpResponse(response)


class ConstituencyFacilities(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_constituency_facilities(kwargs['constituency_id'], True)
        return HttpResponse(response)

    def post(self, request, **kwargs):
        if request.data:
            filters = []
        else:
            print('using filters')
            filters = request.data['filters']

        response = facilities.get_constituency_facilities(kwargs['constituency_id'], True, filters)
        return HttpResponse(response)

class ConstituencySummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_constituency_summary(kwargs['constituency_id'], True)
        return HttpResponse(response)

class WardFacilities(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_facilities(kwargs['ward_id'], True)
        return HttpResponse(response)

    def post(self, request, **kwargs):
        if request.data:
            filters = []
        else:
            filters = request.data['filters']

        response = facilities.get_ward_facilities(kwargs['ward_id'], True,filters)
        return HttpResponse(response)

class WardSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_summary(kwargs['ward_id'], True)
        return HttpResponse(response)

class WardFacilityTypeSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_facility_type_summary(kwargs['ward_id'], True)
        return HttpResponse(response)

class WardKephLevelSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_keph_level_summary(kwargs['ward_id'], True)
        return HttpResponse(response)