from django.conf import settings
from common.analysis import connection
import counties, constituencies
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import os
import psycopg2


def get_all_wards():
    '''return a dataframe of all wards'''
    conn = connection.get_connection()
    all_wards = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM common_ward', con=conn, chunksize=100):
        all_wards = all_wards.append(chunk)

    return all_wards 

def get_constituency_wards_ids_json(constituency_id):
    '''return ids for wards in a constituency'''
    conn = connection.get_connection()
    all_wards = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM common_ward', con=conn, chunksize=100):
        all_wards = all_wards.append(chunk)
    
    

    constituency = constituencies.get_constituency_by_id(constituency_id)
    constituency = constituency.rename(index=str, columns={'id':'constituency_id', 'name': "constituency_name"})
    # import pdb
    # pdb.set_trace()

    constituency_wards = pd.merge(all_wards,constituency, on='constituency_id')
    constituency_wards = constituency_wards[['name','id','constituency_id']]

    return constituency_wards.to_json(orient='records')