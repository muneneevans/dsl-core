from django.conf.urls import url, include
from api import *

app_name= 'indicators'

indicator_api_urls = [
    url(r'^$', IndicatorsListView.as_view(),name='indicators-list'),
    url(r'^indicatorgroups$', IndicatorGroupsListView.as_view(),name='indicatorgroups-list'),
    url(r'^indicatorgroups/(?P<indicatorgroupid>\d+)$', IndicatorGroupsIndicatorsListView.as_view(),name='indicatorgroups-indicators-list'),

]


dataelement_api_urls =[
    url(r'^$', DataElementsListView.as_view(),name='dataelement-list'),
   
    url(r'^(?P<dataelement_id>\w+)/$', DataElementDetailView.as_view(),name='dataelement-details'),

    url(r'^(?P<dataelement_id>\w+)/datavalues$', DataElementDataValuesListView.as_view(),name='dataelement-datavalue-list'),
]

category_combo_api_urls = [
    url(r'^$', CategoryOptionCombos.as_view(),name='categoryoptioncombos-list'),
    url(r'^(?P<category_option_combo_id>\w+)/$', CategoryOptionComboDetailView.as_view(),name='dataelement-details'),
]

datavalue_api_urls = [
    url(r'^facility/(?P<facility_id>[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})/dataelement/(?P<dataelement_id>\w+)/$', FacilityDataElementDataValues.as_view(),name='facility-dataelement-detavalues'),
    url(r'^facility/indicator/$', FacilityIndicatorDataValues.as_view(),name='facility-indicator-datavalues'),
    url(r'^ward/indicator/$', WardIndicatorDataValues.as_view(),name='ward-indicator-datavalues'),
]

periods_api_urls = [
    url(r'^year/(?P<year>\w+)/$', PeriodsListView.as_view(),name='periolds-view'),
    url(r'^periodtypes/$', PeriodTypesListView.as_view(),name='periold-types-view'),
]

api_urls = [
    url(r'^indicators/', include(indicator_api_urls)),
    url(r'^dataelements/', include(dataelement_api_urls)),
    url(r'^datavalues/', include(datavalue_api_urls)),
    url(r'^periods/', include(periods_api_urls)),
    url(r'^categoryoptioncombos/', include(category_combo_api_urls)),


]

urlpatterns = [
    url(r'^api/', include(api_urls)),
]