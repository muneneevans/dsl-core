from common.analysis import connection
from maps.analysis import counties, constituencies, wards
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json


#get facility data types
def get_facility_types_codes(in_json=False):
    '''return all facility typess'''
    conn = connection.get_connection()
    all_facility_types = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM facilities_facilitytype', con=conn, chunksize=100):
        all_facility_types = all_facility_types.append(chunk)
    
    all_facility_types = all_facility_types[['id','name']]

    if in_json:
        return all_facility_types.to_json(orient='records')
    else:
        return all_facility_types


#get facility keph levels
def get_facility_keph_levels_codes(in_json=False):
    '''return all facility keph levels'''
    conn = connection.get_connection()
    all_keph_levels = DataFrame()
    for chunk in pd.read_sql('SELECT * FROM facilities_kephlevel', con=conn, chunksize=100):
        all_keph_levels = all_keph_levels.append(chunk)
    
    all_keph_levels = all_keph_levels[['id','name']]
    
    if in_json:
        return all_keph_levels.to_json(orient='records')
    else:
        return all_keph_levels

#get all facilities
def get_all_facilities():
    conn = connection.get_connection()

    #get all facilieits and merge
    all_facilities = DataFrame()
    for chunk in pd.read_sql('SELECT * FROM facilities_facility', con=conn, chunksize=100):
        all_facilities = all_facilities.append(chunk)

    return all_facilities

#get all the facilities in a ward
def get_ward_facilities(ward_id, in_json=False):
    '''return ids for facilities in a ward'''
    conn = connection.get_connection()
    all_facilities = DataFrame()
    ward = wards.get_ward_by_id(ward_id)
    constituency = constituencies.get_constituency_by_id(ward['constituency_id'].values[0])

    county = counties.get_county_code_by_id(constituency['county_id'].values[0])

    query = "SELECT * FROM facilities_facility WHERE ward_id = '%s' ;" %(ward_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=100):
        all_facilities = all_facilities.append(chunk)
    
    # import pdb
    # pdb.set_trace()
    all_facilities['ward_name'] = ward['name']
    all_facilities['constituency_name'] = constituency['name'].values[0]
    all_facilities['constituency_id'] = constituency.index.values[0]
    all_facilities['county_name'] = county['name'].values[0]
    all_facilities['county_id'] = county.index.values[0]
    if in_json:
        return all_facilities.to_json(orient='records')
    else:
        return all_facilities

#get facilities in ward
def get_constituency_facilities(constituency_id, in_json=False):
    conn = connection.get_connection()
    #get all the wards for the county
    constituency = constituencies.get_constituency_by_id(constituency_id)

    #get all the wards for the constituency
    all_wards = wards.get_constituency_wards(constituency_id) 
    
    all_facilities = DataFrame()
    for index, ward in all_wards.iterrows():
        all_facilities = all_facilities.append(get_ward_facilities(ward['id']))
             

    if in_json:
        return all_facilities.to_json(orient='records')
    else:
        return all_facilities

#get all the facilities in a county
def get_county_facilities(county_id, in_json=False):
    conn = connection.get_connection()
    county = counties.get_county_code_by_id(county_id)
    
    #get constituencies in the county
    county_constituencies = constituencies.get_county_constituency_codes(county_id)
    county_constituencies = county_constituencies.rename(index=str, columns={'id':'constituency_id', 'name': "constituency_name"})
    
    #get all the wards for the county
    all_wards = DataFrame()
    for index, constituency in county_constituencies.iterrows():        
        all_wards = all_wards.append(wards.get_constituency_wards(constituency['constituency_id']) )    
    
    all_facilities = DataFrame()
    for index, ward in all_wards.iterrows():
        all_facilities = all_facilities.append(get_ward_facilities(ward['id']))
            
    all_facilities['county_name'] = county['name']
    all_facilities['county_id'] = county['id']

    if in_json:
        return all_facilities.to_json(orient='records')
    else:
        return all_facilities

#get constituency summaries
def get_constituency_summary(constituency_id, in_json=False):
    '''return a summary of beds and cots per county'''
    constituency_facilities = get_constituency_facilities(constituency_id)
    
    constituency_facilities['number_of_facilities'] = 1
    constituency_summary = constituency_facilities.groupby(['ward_id'],as_index=False).sum()[
        ['number_of_beds','number_of_cots','number_of_facilities','ward_id']]

    
    if in_json:
        return constituency_summary.to_json(orient='records')
    else:
        return constituency_summary

#get county summaries
def get_county_summary(county_id, in_json=False):
    '''return a summary of beds and cots per county'''
    county_facilities = get_county_facilities(county_id)
    
    county_facilities['number_of_facilities'] = 1
    county_summary = county_facilities.groupby(['constituency_id','constituency_name'],as_index=False).sum()[
        ['number_of_beds','number_of_cots','number_of_facilities','constituency_id','constituency_name']]
    
    if in_json:
        return county_summary.to_json(orient='records')
    else:

        return county_summary
    
#get a specific facility
def get_facility_by_id(facility_id, in_json=False):
    '''returns a facility matching the facility id '''
    conn = connection.get_connection()
    all_facilities = pd.DataFrame()
    query = "SELECT name, code FROM facilities_facility WHERE id = '%s' ;" %(facility_id)    
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_facilities = all_facilities.append(chunk)

    facility = all_facilities.head(1)

    if in_json:
        return facility.to_json(oreint='records')
    else:
        return facility