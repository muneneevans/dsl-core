from common.analysis import connection
from maps.analysis import counties, constituencies, wards
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json


#get all job types
def get_job_types(in_json=False):
    ''' return a list of all job types
        returns a dataframe or json string in record orientation '''
    query = ''' SELECT dataelementname as name, dataelementid as id, uid, cadreid as cadreId FROM dim_ihris_dataelement '''
    all_job_types = pd.read_sql(query, connection.get_connection())
    
    if in_json:
        return all_job_types.to_json(orient='records')
    else:
        return all_job_types