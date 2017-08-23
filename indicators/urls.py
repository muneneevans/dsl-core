from django.conf.urls import url, include
from api import *

app_name= 'indicators'

dataelement_api_urls =[
    url(r'^$', DataElementsListView.as_view(),name='dataelement-list'),
   
    url(r'^(?P<dataelement_id>\w+)/$', DataElementDetailView.as_view(),name='dataelement-details'),

    url(r'^(?P<dataelement_id>\w+)/datavalues$', DataElementDataValuesListView.as_view(),name='dataelement-datavalue-list'),
]

datavalue_api_urls = [
    url(r'^facility/(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/dataelement/(?P<dataelement_id>\w+)/$', FacilityDataElementDataValues.as_view(),name='facility-dataelement-detavalues'),
]

api_urls = [
    url(r'^dataelements/', include(dataelement_api_urls)),
    url(r'^datavalues/', include(datavalue_api_urls)),

]

urlpatterns = [
    url(r'^api/', include(api_urls)),
]