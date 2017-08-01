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

#get all the facilities in a county
def get_county_facilities(county_id, in_json=False):
    conn = connection.get_connection()
    county = counties.get_county_code_by_id(county_id)
    
    #get county_constituencies in the county
    county_constituencies = constituencies.get_county_constituency_codes(county_id)
    county_constituencies = county_constituencies.rename(index=str, columns={'id':'constituency_id', 'name': "constituency_name"})
    
    #get all the wards for the county
    all_wards = wards.get_all_wards()
    
    #merge with the consitituencies
    county_wards = pd.merge(all_wards,county_constituencies,on='constituency_id')
    county_wards = county_wards.rename(index=str, columns={'id': 'ward_id', 'name': 'ward_name'})
    
    #get all facilieits and merge
    all_facilities = DataFrame()
    for chunk in pd.read_sql('SELECT * FROM facilities_facility', con=conn, chunksize=100):
        all_facilities = all_facilities.append(chunk)
    
    
    county_facilities = pd.merge(all_facilities,county_wards, on='ward_id')
    county_facilities = county_facilities[['id','name','official_name','number_of_beds','number_of_cots','approved' ,'facility_type_id','keph_level_id','ward_id']]

    if in_json:
        return county_facilities.to_json(orient='records')
    else:
        return county_facilities

#get all the facilities in a constituency
def get_constituency_facilities(constituency_id, in_json=False):
    conn = connection.get_connection()
    constituency = constituencies.get_constituency_by_id(constituency_id)

    #get all wards in the constituency
    constituency_wards = wards.get_constituency_wards(constituency_id)
    #get all facilities
    all_facilities = get_all_facilities()

    constituency_facilities = pd.merge(all_facilities,constituency_wards, on='ward_id')
    county_facilities = county_facilities[['id','name','official_name','number_of_beds','number_of_cots','approved' ,'facility_type_id','keph_level_id','ward_id']]

    if in_json:
        return county_facilities.to_json(orient='records')
    else:
        return county_facilities
