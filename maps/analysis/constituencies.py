from django.conf import settings
from common.analysis import connection
import counties
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

def get_constituency_by_id(constituency_id):
    conn = connection.get_connection()
    all_constituencies = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM common_constituency', con=conn, chunksize=100):
        all_constituencies = all_constituencies.append(chunk)
    
    constituency = all_constituencies[all_constituencies['id']==constituency_id]

    return constituency

def get_county_constituency_codes_json(county_id):
    '''return codes for constituencies in county'''
    conn = connection.get_connection()
    all_constituencies = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM common_constituency', con=conn, chunksize=100):
        all_constituencies = all_constituencies.append(chunk)
    
    county = counties.get_county_code_by_id(county_id)
    county = county.rename(index=str, columns={"id": "county_id", 'name': 'county_name'})
    county_constituencies = pd.merge(all_constituencies,county, on='county_id')
    county_constituencies = county_constituencies[['name','id','county_id']]
    
    return county_constituencies.to_json(orient='records')

def get_county_constituency_codes(county_id):
    '''return codes for constituencies in county'''
    conn = connection.get_connection()
    all_constituencies = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM common_constituency', con=conn, chunksize=100):
        all_constituencies = all_constituencies.append(chunk)
    
    county = counties.get_county_code_by_id(county_id)
    county = county.rename(index=str, columns={"id": "county_id", 'name': 'county_name'})
    county_constituencies = pd.merge(all_constituencies,county, on='county_id')
    county_constituencies = county_constituencies[['name','id','county_id']]
    
    return county_constituencies
