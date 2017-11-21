from django.conf.urls import url, include
from api import *

app_name = 'hr'

staff_urls=[
    url(r'^jobtypes/$',JobTypesView.as_view(), name='job-types'),
    url(r'^cadres/$',CadresView.as_view(), name='cadres'),
]

facility_urls =[
    url(r'^(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/$',FacilityStaffView.as_view(), name='facility-staff'),
    url(r'^(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/jobtype/(?P<job_type_id>\w+)/$',FacilityJobTypeView.as_view(), name='facility-job-type'),
]

api_urls=[
    url(r'^staff/', include(staff_urls)),
    url(r'^facility/', include(facility_urls)),
]

urlpatterns = [
    url(r'^api/', include(api_urls))
]