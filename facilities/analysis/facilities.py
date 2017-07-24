from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json


#get facility data types
def get_facility_types_codes(injson=False):
    '''return codes for constituencies in county'''
    conn = connection.get_connection()
    all_facility_types = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM facilities_facilitytype', con=conn, chunksize=100):
        all_facility_types = all_facility_types.append(chunk)
    
    all_facility_types = all_facility_types[['id','name']]

    if injson:
        return all_facility_types.to_json(orient='records')
    else:
        return all_facility_types