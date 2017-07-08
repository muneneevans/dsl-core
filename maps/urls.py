from django.conf.urls import url, include
from maps.api import *

app_name='maps'

Country_api_urls = [

    url(r'^$', CountryListView.as_view(), name='country-list'),


    # url(r'^(?P<country_represented>[a-zA-Z0-9]+)/plain$', CountryPlainMapView.as_view(), name="country-plain-map"),
]

county_api_urls=[

    url(r'^map$', KenyaCountyMapView.as_view(), name='kenya-county-map'),

    url(r'^list$', KenyaCountyList.as_view(), name='kenya-county-list'),

    url(r'^(?P<county_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/constituencies/$', CountyConstituencyList.as_view(), name='county-constituency-list'),

]



api_urls = [
    url(r'^countries/', include(Country_api_urls)),
    url(r'^counties/', include(county_api_urls)),
]

urlpatterns = [
    url(r'^', include(api_urls)),

    url(r'^api/', include(api_urls)),
]
