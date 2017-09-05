from rest_framework import generics
from rest_framework.generics import ListAPIView
from analysis import facilities
from django.http import HttpResponse, JsonResponse


class FaciltyTypeListView(ListAPIView):
    def get(self, request ):
        result = facilities.get_facility_types_codes(True)
        return HttpResponse(result)

class FacilityKephLevelsView(ListAPIView):
    def get(self, request):
        result = facilities.get_facility_keph_levels_codes(True)
        return HttpResponse(result)

class CountyFacilities(ListAPIView):
    def get(self, request, **kwargs):
        result = facilities.get_county_facilities(kwargs['county_id'],True)
        return HttpResponse(result)

class CountySummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_county_summary(kwargs['county_id'], True)
        return HttpResponse(response)

class ConstituencyFacilities(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_constituency_facilities(kwargs['constituency_id'], True)
        return HttpResponse(response)

class ConstituencySummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_constituency_summary(kwargs['constituency_id'], True)
        return HttpResponse(response)

class WardFacilities(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_facilities(kwargs['ward_id'], True)
        return HttpResponse(response)

class WardSummary(ListAPIView):
    def get(self, request, **kwargs):
        response = facilities.get_ward_summary(kwargs['ward_id'], True)
        return HttpResponse(response)