from django.conf import settings
from common.analysis import connection
import numpy as np
import dataelements
import pandas as pd
from pandas import DataFrame
from . import orgunits
from . import dataelements

def get_all_datavalues(in_json=False):
    '''return all datavalues in the datase'''
    conn = connection.get_connection()
    all_datavalues = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM fact_dhis_datavalue LIMIT 50000', con=conn, chunksize=1000):
        all_datavalues = all_datavalues.append(chunk)
    
    if in_json:
        return all_datavalues.to_json(orient='records')
    else:
        return all_datavalues

def get_dataelement_datavalues(dataelement_id, in_json=False):
    '''return all data values in a dataelement'''
    # conn = connection.get_connection()
    all_datavalues = get_all_datavalues()

    dataelement = dataelements.get_dataelement_by_id(dataelement_id)

    dataelement_datavalues = pd.merge(all_datavalues, dataelement, on='dataelementid')

    dataelement_datavalues = dataelement_datavalues[['periodid','sourceid','categoryoptioncomboid','attributeoptioncomboid','value']]
    if in_json:
        return dataelement_datavalues.to_json(orient='records')
    else:
        return dataelement_datavalues

def get_facility_dataelement_datavalues(dataelement_id, facility_id, in_json=False):
    conn = connection.get_connection()
    orgnaization_unit = orgunits.get_facility_org_units(facility_id)
    dataelement = dataelements.get_dataelement_by_id(dataelement_id)
    all_datavalues = DataFrame()
    
    query = "SELECT * FROM fact_dhis_datavalue WHERE dataelementid = %s AND sourceid = %s ;" %(dataelement_id, orgnaization_unit['organisationunitid'][0])
    for chunk in pd.read_sql(query, con=conn , chunksize=10000):
        all_datavalues = all_datavalues.append(chunk)
    
    if in_json:
        return all_datavalues.to_json(orient='records')
    else:
        return all_datavalues
