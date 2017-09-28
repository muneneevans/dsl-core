from django.conf.urls import url, include
from api import *

app_name='facilities'

facility_urls = [

    url(r'^facilitytypes/$',FaciltyTypeListView.as_view(), name='facility-type-list'),
    url(r'^kephlevels/$',FacilityKephLevelsView.as_view(), name='facility-keph-levels'),
    
    url(r'^country/summary/$',CountrySummary.as_view(), name='country-summary'),
    url(r'^country/facilitytypes/summary/$',CountryFacilityTypeSummary.as_view(), name='country-facilitytypes-summary'),

    url(r'^county/(?P<county_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/facilities/$',CountyFacilities.as_view(), name='county-facilities'),
    url(r'^county/(?P<county_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/summary/$',CountySummary.as_view(), name='county-summary'),
    url(r'^constituency/(?P<constituency_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/facilities/$',ConstituencyFacilities.as_view(), name='constituency-facilities'),
    url(r'^constituency/(?P<constituency_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/summary/$',ConstituencySummary.as_view(), name='constituency-summary'),
    url(r'^ward/(?P<ward_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/facilities/$',WardFacilities.as_view(), name='ward-facilities'),
    url(r'^ward/(?P<ward_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/summary/$',WardSummary.as_view(), name='ward-summary'),
    url(r'^(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',FacilityDetails.as_view(), name='ward-summary'),

]

urlpatterns = [
    url(r'^api/', include(facility_urls)),
]