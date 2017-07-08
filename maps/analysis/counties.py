
from django.conf import settings
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import os
import psycopg2

def get_settings():

    return settings.DW_DATABASE

def get_connection():
    config = settings.DW_DATABASE
    conn_str = "host={} dbname={} user={} password={}".format(
                config['host'], config['database'], 
                config['user'], config['passw'])
    
    try:
        conn = psycopg2.connect(conn_str)
        return conn
    except Exception:
        return Exception.message

def get_county_code_by_id(county_id):
    conn = get_connection()
    all_counties = pd.DataFrame()
    for chunk in pd.read_sql('SELECT * FROM common_county', con=conn, chunksize=100):
        all_counties = all_counties.append(chunk)

    all_counties = all_counties[all_counties['id']==county_id]
    
    return all_counties

def get_county_codes():
    ''' returns a dataframe of all counties '''
    conn = get_connection()
    all_counties = pd.DataFrame()
    for chunk in pd.read_sql('SELECT * FROM common_county', con=conn, chunksize=100):
        all_counties = all_counties.append(chunk)

    all_counties = all_counties[['name','id']]
    return all_counties.to_json(orient='records')
    # return all_counties.to_json(orient='records')
