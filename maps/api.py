from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView


from .serializers import *
from .models import *


class CountryListView(generics.ListAPIView):
    model = Country

    queryset = Country.objects.all()
    serializer_class = CountryInlineSerializer

class CountryPlainMapView(generics.RetrieveAPIView):
    models = CountryMap
    queryset = CountryMap.objects.all()
    serializer_class = CountryMapInlineSerializer
    lookup_field = 'country_represented'
