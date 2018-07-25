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

def get_constituency_by_id(constituency_id, in_json=False):
    conn = connection.get_connection()
    all_constituencies = pd.DataFrame()
    query = "SELECT * FROM common_constituency WHERE id = '%s' ;" %(constituency_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=100):
        all_constituencies = all_constituencies.append(chunk)

    # all_constituencies = all_constituencies[all_constituencies['id']==constituency_id]
    # import pdb
    # pdb.set_trace()


    if in_json:
        return all_constituencies.head(1).to_json(orient="records")
    else:
        return all_constituencies.head(1)


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

def get_county_constituency_codes(county_id, in_json=False):
    '''return codes for constituencies in county'''
    conn = connection.get_connection()
    all_constituencies = DataFrame()
    county = counties.get_county_code_by_id(county_id)

    query = "SELECT * FROM common_constituency WHERE county_id = '%s' ;" %(county_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=1000):
        all_constituencies = all_constituencies.append(chunk)

    all_constituencies['county_name'] = county['name']
    all_constituencies = all_constituencies[['name','id','county_id', 'county_name']]

    if in_json:
        return all_constituencies.to_json(orient='records')
    else:
        return all_constituencies
