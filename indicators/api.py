from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from analysis import dataelements


class DataElementsListView(ListAPIView):
    def get(self, request):
        result = dataelements.get_all_dataelements(True)

        return HttpResponse(result)