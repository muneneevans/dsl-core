from django.conf.urls import url, include
from api import *

app_name = 'hr'

staff_urls=[
    url(r'^jobtypes/$',JobTypesView.as_view(), name='job-types'),
    url(r'^cadres/$',CadresView.as_view(), name='cadres'),
    url(r'^facility/(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',FacilityStaffView.as_view(), name='facility-staff'),
]

api_urls=[
    url(r'^staff/', include(staff_urls)),
]

urlpatterns = [
    url(r'^api/', include(api_urls))
]