from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from analysis import dataelements, datavalues


class DataElementsListView(ListAPIView):
    def get(self, request):
        result = dataelements.get_all_dataelements(True)

        return HttpResponse(result)

class DataElementDataValuesListView(ListAPIView):
    def get(self, request, **kwargs):
        result = datavalues.get_dataelement_datavalues(kwargs['dataelement_id'],True)

        return HttpResponse(result)