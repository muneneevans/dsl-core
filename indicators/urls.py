from django.conf.urls import url, include
from api import *

app_name= 'indicators'

dataelement_api_urls =[
    url(r'^$', DataElementsListView.as_view(),name='dataelement-list'),
]

api_urls = [
    url(r'^datalements/', include(dataelement_api_urls)),

]

urlpatterns = [
    url(r'^api/', include(api_urls)),
]