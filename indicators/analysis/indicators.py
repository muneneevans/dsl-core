from django.conf import settings
from common.analysis import connection
import numpy as np
import dataelements
import pandas as pd
from pandas import DataFrame


def get_indicator_groups(in_json=False):
    '''return a list of all indicator groups'''
    conn = connection.get_connection()
    
    all_indicator_groups = DataFrame()
    
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_indicatorgroup', con=conn, chunksize=100):
        all_indicator_groups = all_indicator_groups.append(chunk)
    
    if in_json:
        return all_indicator_groups.to_json(orient='records')
    else:
        return all_indicator_groups

def get_indicator_group_by_id(indicator_group_id):
    '''return a single indicator group matching the id'''
    conn = connection.get_connection()
    
    all_indicator_groups = DataFrame()
    
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_indicatorgroup', con=conn, chunksize=100):
        all_indicator_groups = all_indicator_groups.append(chunk)
    
    single_indicator = all_indicator_groups[all_indicator_groups['indicatorgroupid']==indicator_group_id]
    return single_indicator

def get_indicator_group_members(indicator_group_id):
    '''return all indicators in an indicator group'''
    conn = connection.get_connection()
    
    #get the indicator group
    indicator_group = get_indicator_group_by_id(indicator_group_id)
    indicator_group = indicator_group.rename(index=str, columns={'name': 'indicator_group_name'})
    
    all_indicator_group_members = DataFrame()
    
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_indicatorgroupmembers', con=conn, chunksize=100):
        all_indicator_group_members = all_indicator_group_members.append(chunk)
    
    indicator_group_members = pd.merge(all_indicator_group_members, indicator_group, on='indicatorgroupid')
    
    return indicator_group_members

def get_indicator_group_indicators(indicator_group_id, in_json=False):
    '''get all indicators in an indicator group'''
    conn= connection.get_connection()
    #get indicator memmbers
    indicator_memmber = get_indicator_group_members(indicator_group_id)
    
    all_indicators = DataFrame()
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_indicator', con=conn, chunksize=100):
        all_indicators = all_indicators.append(chunk)
    
    indicators = pd.merge(all_indicators, indicator_memmber, on='indicatorid')
    
    if in_json:
        return indicators.to_json(orient='records')
    else:
        return indicators


def get_indicators(in_json=False):
    '''return a list of all indicator groups'''
    conn = connection.get_connection()
    
    all_indicators = DataFrame()
    
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_indicator', con=conn, chunksize=10000):
        all_indicators = all_indicators.append(chunk)
    
    if in_json:
        return all_indicators.to_json(orient='records')
    else:
        return all_indicators