from django.conf.urls import url, include
from maps.api import *

app_name='maps'

Country_api_urls = [

    url(r'^$', CountryListView.as_view(), name='country-list'),

    url(r'^kenya/county$', KenyaCountyMapView.as_view(), name='kenya-county-map'),

    # url(r'^(?P<country_represented>[a-zA-Z0-9]+)/plain$', CountryPlainMapView.as_view(), name="country-plain-map"),
]



api_urls = [
    url(r'^countries/', include(Country_api_urls)),
]

urlpatterns = [
    url(r'^', include(api_urls)),

    url(r'^api/', include(api_urls)),
]
