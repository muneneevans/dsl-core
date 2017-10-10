from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from analysis import dataelements, datavalues, category_option_combos, periods, indicators


class IndicatorsListView(ListAPIView):
    def get(self , request):
        response = indicators.get_indicators(True)
        return HttpResponse(response)

class IndicatorGroupsListView(ListAPIView):
    def get(self , request):
        response = indicators.get_indicator_groups(True)
        return HttpResponse(response)

class IndicatorGroupsIndicatorsListView(ListAPIView):
    def get(self, request, **kwargs):
        response = indicators.get_indicator_group_indicators(int(kwargs['indicatorgroupid']), True)
        return HttpResponse(response)

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

class PeriodsListView(ListAPIView):
    def get(self, request, **kwargs):
        response = periods.get_year_periods(kwargs['year'],True)
        return HttpResponse(response)

class PeriodTypesListView(ListAPIView):
    def get(self, request):
        response = periods.get_period_types(True)
        return HttpResponse(response)