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

#get all the wards in a constituency
def get_constituency_wards(constituency_id, in_json=False):
    '''return ids for wards in a constituency'''
    conn = connection.get_connection()
    all_wards = DataFrame()
    constituency = constituencies.get_constituency_by_id(constituency_id)
    
    query = "SELECT * FROM common_ward WHERE constituency_id = '%s' ;" %(constituency_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=100):
        all_wards = all_wards.append(chunk)
    
    all_wards['constituency_name'] = constituency['name']
    all_wards = all_wards[['name','id','constituency_id', 'constituency_name']]

    if in_json:
        return all_wards.to_json(orient='records')
    else:
        return all_wards

def get_ward_by_id(ward_id, in_json=False):
    conn = connection.get_connection()
    all_wards = pd.DataFrame()
    query = "SELECT * FROM common_ward WHERE id = '%s' ;" %(ward_id)   
    wards =pd.read_sql(query, con=conn, chunksize=10)
    for chunk in wards:
        all_wards = all_wards.append(chunk)
  
    ward = DataFrame([], columns=['ward_id','ward_name'])
    ward.loc[0,'ward_id'] = all_wards['id'][0]  
    ward.loc[0,'ward_name'] = all_wards['name'][0]  
    ward.loc[0,'constituency_id'] = all_wards['constituency_id'][0]  

    if in_json:
        return ward.to_json(orient='records')
    else:
        return ward