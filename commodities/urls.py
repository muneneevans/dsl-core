from django.conf.urls import url, include
from api import *

app_name = 'commodities'

product_urls = [
    url(r'^$',ProductsListView.as_view(), name='products-list'),
]

api_urls = [
    url(r'^products/',include(product_urls)),
    
]
urlpatterns = [
    url(r'^api/', include(api_urls))
]