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
def get_ward_facilities(ward_id, in_json=False, filters=None):
    '''return ids for facilities in a ward'''
    conn = connection.get_connection()
    all_facilities = DataFrame()
    ward = wards.get_ward_by_id(ward_id)
    constituency = constituencies.get_constituency_by_id(ward['constituency_id'].values[0])
    county = counties.get_county_code_by_id(constituency['county_id'].values[0])


    query = "SELECT * FROM facilities_facility WHERE ward_id = '%s' ;" %(ward_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=100):
        all_facilities = all_facilities.append(chunk)
    
    if filters:
        for key, value in filters.iteritems():            
            all_facilities = all_facilities[all_facilities[key] == value]

    
    all_facilities['ward_name'] = ward['ward_name'][0]
    all_facilities['constituency_name'] = constituency['name'][0]
    all_facilities['constituency_id'] = constituency['id'][0]
    all_facilities['county_name'] = county['name'][0]
    all_facilities['county_id'] = county['id'][0]


    if in_json:
        return all_facilities.to_json(orient='records')
    else:
        return all_facilities

#get facilities in ward
def get_constituency_facilities(constituency_id, in_json=False, filters=None):
    conn = connection.get_connection()
    #get all the wards for the county
    constituency = constituencies.get_constituency_by_id(constituency_id)

    #get all the wards for the constituency
    all_wards = wards.get_constituency_wards(constituency_id) 
    
    all_facilities = DataFrame()
    for index, ward in all_wards.iterrows():
        all_facilities = all_facilities.append(get_ward_facilities(ward['id'],filters=filters))
             

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


#get ward summaries
def get_ward_summary(ward_id, in_json=False):
    '''return a summary of facilities in  ward'''
    ward_facilities = get_ward_facilities(ward_id)

    ward_facilities['number_of_facilities'] = 1
    ward_summary = ward_facilities.groupby(['id','name'], as_index=False).sum()[
        ['number_of_beds','number_of_cots','number_of_facilities','id','name']]
    
    if in_json:
        return ward_summary.to_json(orient='records')
    else:
        return ward_summary

#get constituency summaries
def get_constituency_summary(constituency_id, in_json=False):
    '''return a summary of beds and cots per county'''
    constituency_facilities = get_constituency_facilities(constituency_id)
    
    constituency_facilities['number_of_facilities'] = 1
    constituency_summary = constituency_facilities.groupby(['ward_id','ward_name'],as_index=False).sum()[
        ['number_of_beds','number_of_cots','number_of_facilities','ward_id','ward_name']]

    
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

def get_country_summary(in_json=False):
    '''return a summary of beds cots and facilities for all counties'''
    conn = connection.get_connection()
    country_summary = pd.DataFrame()
    query = '''SELECT  common_county.id AS county_id, COUNT(facilities_facility.id) as number_of_facilities , SUM(number_of_beds) AS number_of_beds, SUM(number_of_cots) AS number_of_cots
        FROM facilities_facility , common_ward , common_constituency , common_county 
        WHERE facilities_facility.ward_id = common_ward.id 
            AND common_ward.constituency_id = common_constituency.id 
            AND common_constituency.county_id = common_county.id
        GROUP BY(common_county.id)'''
    country_summary = pd.read_sql(query, con=conn)
    
    all_counties = counties.get_all_counties()
    response = pd.merge(country_summary,all_counties, left_on='county_id', right_on='id')

    if in_json:
        return response.to_json(orient='records')
    else:
        return response

#get summary of facility types by county
def get_country_facility_type_summary(in_json=False):
    '''return a table of facility types per county'''
    conn = connection.get_connection()
    all_facility_types = pd.DataFrame()
    facility_types_query = '''SELECT facilities_facility.id as count, common_county.name AS county_name, facilities_facilitytype.name  as facility_type_name
        FROM facilities_facility , common_ward , common_constituency , common_county, facilities_facilitytype 
        WHERE facilities_facility.ward_id = common_ward.id 
            AND common_ward.constituency_id = common_constituency.id
            AND facilities_facilitytype.id = facilities_facility.facility_type_id
            AND common_constituency.county_id = common_county.id'''
    all_facility_types = pd.read_sql(facility_types_query, con=conn).groupby(['county_name','facility_type_name']).count().unstack().T.fillna(0).xs('count', axis=0, drop_level=True).T
    
    
    if in_json:
        return all_facility_types.to_json(orient='table')
    else:
        return all_facility_types

#get a specific facility
def get_facility_by_id(facility_id, in_json=False):
    '''returns a facility matching the facility id '''
    conn = connection.get_connection()
    all_facilities = pd.DataFrame()
    query = "SELECT * FROM facilities_facility WHERE id = '%s' ;" %(facility_id)    
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_facilities = all_facilities.append(chunk)

    facility= all_facilities.head(1)

    if in_json:
        return facility.to_json(orient='records')
    else:
        return facility
