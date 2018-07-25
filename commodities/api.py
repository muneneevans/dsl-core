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
    def post(self, request, **kwargs):
        filters = request.data['filters']
        required_filters = [ 'year']
        for r_filter in required_filters:
            if not r_filter in filters.keys():
                return  JsonResponse({'status':'bad request','message':"missing attribute: "+ r_filter}, status=400)
        
        response = products.get_facility_year_products(kwargs['facility_id'],filters['year'], True)
        return HttpResponse(response)