from rest_framework import generics
from rest_framework.generics import ListAPIView
from analysis import products
from django.http import HttpResponse, JsonResponse
import json

class ProductsListView(ListAPIView):
    def get(self, request):
        response = products.get_all_products(True)
        return HttpResponse(response)

class FacilityProductsListView(ListAPIView):
    def get(self, request, **kwargs):
        response = products.get_facility_products(kwargs['facility_id'], True)
        return HttpResponse(response)
        