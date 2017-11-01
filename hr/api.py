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