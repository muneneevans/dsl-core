from django.conf import settings
from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame


def get_all_dataelements(in_json=False):
    '''return a all dataelements in the database'''
    conn = connection.get_connection()
    all_dataelements = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM dim_dhis_dataelement', con=conn, chunksize=100):
        all_dataelements = all_dataelements.append(chunk)
    
    all_dataelements = all_dataelements[['dataelementid','dataelementname','description','domaintype','uid','valuetype']]

    if in_json:
        return all_dataelements.to_json(orient='records')
    else:
        return all_dataelements

def get_dataelement_by_id(data_element_id, in_json=False):
    '''retuanr a single datatelement matching the id'''
    conn = connection.get_connection()
    all_data_elements = pd.DataFrame()
    query = "SELECT * FROM dim_dhis_dataelement WHERE dataelementid = %s ;" %(data_element_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_data_elements = all_data_elements.append(chunk)

    data_element = all_data_elements.head(1)[['dataelementname','dataelementid','valuetype','domaintype','aggregationtype']]
    
    if in_json:
        return data_element.to_json(orient='records')
    else:
        return data_element


