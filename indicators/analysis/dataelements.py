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

def get_all_dataelement_by_id(dataelement_id,in_json=False):
    '''return a all dataelements in the database'''
    conn = connection.get_connection()
    all_dataelements = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM dim_dhis_dataelement', con=conn, chunksize=100):
        all_dataelements = all_dataelements.append(chunk)
    
    all_dataelements = all_dataelements[all_dataelements['dataelementid'] == dataelement_id]
    all_dataelements = all_dataelements[['dataelementid','dataelementname','description','domaintype','uid','valuetype']]

    if in_json:
        return all_dataelements.to_json(orient='records')
    else:
        return all_dataelements

