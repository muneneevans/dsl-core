from common.analysis import connection
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
    conn = connection.get_connection()
    all_counties = pd.DataFrame()
    query = "SELECT * FROM common_county WHERE id = '%s' ;" %(county_id)   
    for chunk in pd.read_sql(query, con=conn, chunksize=100):
        all_counties = all_counties.append(chunk)

    all_counties = all_counties[all_counties['id']==county_id]
    
    return all_counties.head(1)

def get_county_codes():
    ''' returns a dataframe of all counties '''
    conn = get_connection()
    all_counties = pd.DataFrame()
    for chunk in pd.read_sql('SELECT * FROM common_county', con=conn, chunksize=1000):
        all_counties = all_counties.append(chunk)

    all_counties = all_counties[['name','id']]
    return all_counties.to_json(orient='records')
    # return all_counties.to_json(orient='records')


def get_all_counties(in_json=False):
    ''' returns a dataframe of all counties '''
    conn = get_connection()
    all_counties = pd.DataFrame()
    for chunk in pd.read_sql('SELECT * FROM common_county', con=conn, chunksize=1000):
        all_counties = all_counties.append(chunk)

    if in_json:
        return all_counties.to_json(orient='records')
    else:
        return all_counties
    