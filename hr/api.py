from rest_framework import generics
from rest_framework.generics import ListAPIView
from analysis import staff
from django.http import HttpResponse, JsonResponse
import json


class JobTypesView(ListAPIView):
    def get(self, request):
        response = staff.get_job_types(True)
        return HttpResponse(response)

class CadresView(ListAPIView):
    def get(self, request):
        response = staff.get_cadres(True)
        return HttpResponse(response)


class CountryJobTypeView(ListAPIView):
    def get(self, request, **kwargs):
        response = staff.get_country_jobtypes(True)
        return HttpResponse(response)

class CountryCountyStaffView(ListAPIView):
    def get(self, request, **kwargs):
        response = staff.get_country_county_number_of_staff(True)
        return HttpResponse(response)

class FacilityStaffView(ListAPIView):
    def get(self, request, **kwargs):
        response = staff.get_facility_staff(kwargs['facility_id'],True)
        return HttpResponse(response)

class FacilityJobTypeView(ListAPIView):
    def get(self, request, **kwargs):
        response = staff.get_facility_job_type(kwargs['facility_id'], kwargs['job_type_id'], True)
        return HttpResponse(response)

class WardFacilityStaffView(ListAPIView):
    def get(self, request, **kwargs):
        response = staff.get_ward_facility_number_of_staff(kwargs['ward_id'], True)
        return HttpResponse(response)