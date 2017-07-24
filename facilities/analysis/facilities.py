from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json


#get facility data types
def get_facility_types_codes(in_json=False):
    '''return all facility typess'''
    conn = connection.get_connection()
    all_facility_types = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM facilities_facilitytype', con=conn, chunksize=100):
        all_facility_types = all_facility_types.append(chunk)
    
    all_facility_types = all_facility_types[['id','name']]

    if in_json:
        return all_facility_types.to_json(orient='records')
    else:
        return all_facility_types


#get facility keph levels
def get_facility_keph_levels_codes(in_json=False):
    '''return all facility keph levels'''
    conn = connection.get_connection()
    all_keph_levels = DataFrame()
    for chunk in pd.read_sql('SELECT * FROM facilities_kephlevel', con=conn, chunksize=100):
        all_keph_levels = all_keph_levels.append(chunk)
    
    all_keph_levels = all_keph_levels[['id','name']]
    
    if in_json:
        return all_keph_levels.to_json(orient='records')
    else:
        return all_keph_levels
