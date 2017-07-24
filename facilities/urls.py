from django.conf.urls import url, include
from api import *

app_name='facilities'



urlpatterns = [
    url(r'^facilitytypes/$',FaciltyTypeListView.as_view(), name='facility-type-list'),
]