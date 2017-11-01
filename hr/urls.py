from django.conf.urls import url, include
from api import *

app_name = 'hr'

staff_urls=[
    url(r'^jobtypes/$',JobTypesView.as_view(), name='job-types'),
    url(r'^cadres/$',CadresView.as_view(), name='cadres'),
]

api_urls=[
    url(r'^staff/', include(staff_urls)),
]

urlpatterns = [
    url(r'^api/', include(api_urls))
]