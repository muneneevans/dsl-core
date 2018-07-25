from django.conf.urls import url, include
from api import *

app_name = 'commodities'

product_urls = [
    url(r'^$',ProductsListView.as_view(), name='products-list'),
    url(r'^facility/(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',FacilityProductsListView.as_view(), name='facility-products-list'),
]

api_urls = [
    url(r'^products/',include(product_urls)),
    
]
urlpatterns = [
    url(r'^api/', include(api_urls))
]