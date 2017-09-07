from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from analysis import dataelements, datavalues, category_option_combos


class DataElementsListView(ListAPIView):
    def get(self, request):
        response = dataelements.get_all_dataelements(True)

        return HttpResponse(response)

class DataElementDetailView(ListAPIView):
    def get(self, request, **kwargs):
        response = dataelements.get_dataelement_by_id(kwargs['dataelement_id'], True)

        return HttpResponse(response)

class DataElementDataValuesListView(ListAPIView):
    def get(self, request, **kwargs):
        result = datavalues.get_dataelement_datavalues(kwargs['dataelement_id'],True)

        return HttpResponse(result)


class FacilityDataElementDataValues(ListAPIView):
    def get(self, request, **kwargs):
        response = datavalues.get_facility_dataelement_datavalues(kwargs['dataelement_id'],kwargs['facility_id'], True)

        return HttpResponse(response)

class CategoryOptionCombos(ListAPIView):
    def get(self, request):
        response = category_option_combos.get_all_category_option_combos(True)

        return HttpResponse(response)

class CategoryOptionComboDetailView(ListAPIView):
    def get(self, request, **kwargs):
        response = category_option_combos.get_category_option_combo_by_id(kwargs['category_option_combo_id'],True)
        return HttpResponse(response)