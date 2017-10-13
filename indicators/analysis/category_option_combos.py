from django.conf import settings
from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame


def get_all_category_option_combos(in_json=False):
    '''return all catagory combox '''
    conn = connection.get_connection()
    all_category_combos = pd.DataFrame()
    query = "SELECT * FROM dim_dhis_categoryoptioncombo;"
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_category_combos = all_category_combos.append(chunk)
    
    if in_json:
        return all_category_combos.to_json(orient='records')
    else:
        return all_category_combos

def get_category_option_combo_by_id(category_option_combo_id, in_json=False):
    '''return a specific category combo'''
    conn = connection.get_connection()
    all_category_combos = pd.DataFrame()
    query = "SELECT * FROM dim_dhis_categoryoptioncombo WHERE categoryoptioncomboid = %s ;" %(category_option_combo_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_category_combos = all_category_combos.append(chunk)

    category_combo = all_category_combos.head(1)[['categoryoptioncomboid','code']]
    
    if in_json:
        return category_combo.to_json(orient='records')
    else:
        return category_combo


def get_category_option_combo_by_uid(category_option_combo_id, in_json=False):
    ''' get the category option combo that matches the given uid
        returns a dataframe or json string in record orientation '''

    conn = connection.get_connection()
    all_category_option_combos = pd.DataFrame()
    query =  '''SELECT * 
                FROM dim_dhis_categoryoptioncombo
                WHERE uid = '%s'
            ''' %(category_option_combo_id)
    all_category_option_combos =  pd.read_sql(query, con=conn)
        
    if in_json:
        return all_category_option_combos.to_json(orient="records")
    else:
        return all_category_option_combos