from django.conf.urls import url, include
from api import *

app_name='facilities'



urlpatterns = [
    url(r'^facilitytypes/$',FaciltyTypeListView.as_view(), name='facility-type-list'),
    url(r'^kephlevels/$',FacilityKephLevelsView.as_view(), name='facility-keph-levels'),
    url(r'^county/(?P<county_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/facilities/$',CountyFacilities.as_view(), name='county-facilities'),
]