from django.conf.urls import url, include
from api import *

app_name= 'indicators'

dataelement_api_urls =[
    url(r'^$', DataElementsListView.as_view(),name='dataelement-list'),

    url(r'^(?P<dataelement_id>\w+)/datavalues$', DataElementDataValuesListView.as_view(),name='dataelement-datavalue-list'),
]

datavalue_api_urls = [

]

api_urls = [
    url(r'^datalements/', include(dataelement_api_urls)),
    url(r'^datavalues/', include(dataelement_api_urls)),

]

urlpatterns = [
    url(r'^api/', include(api_urls)),
]