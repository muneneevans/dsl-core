from common.analysis import connection
from maps.analysis import counties, constituencies, wards
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json


#get all job types
def get_job_types(in_json=False):
    ''' return a list of all job types
        returns a dataframe or json string in record orientation '''
    query = ''' SELECT dataelementname as name, dataelementid as id, uid, cadreid as cadreId FROM dim_ihris_dataelement '''
    all_job_types = pd.read_sql(query, connection.get_connection())
    
    if in_json:
        return all_job_types.to_json(orient='records')
    else:
        return all_job_types


#get all cadres
def get_cadres(in_json=False):
    ''' return a list of all job types
        returns a dataframe or json string in record orientation '''
    query = ''' SELECT cadreid as id, cadrename as name FROM dim_ihris_cadre '''
    all_cadres = pd.read_sql(query, connection.get_connection())
    
    if in_json:
        return all_cadres.to_json(orient='records')
    else:
        return all_cadres

def get_facility_staff(facility_id, in_json=False):
    ''' Return a list of all products that have been ordered by the facility'''
    query = """ SELECT a.value, b.dataelementname as jobType, c.name 
                FROM fact_ihris_datavalue a, dim_ihris_dataelement b, facilities_facility c
                WHERE a.mflcode = c.code 
                    AND a.dataelementid = b.uid
                    AND c.id = '%s' """%(facility_id)
    staff = pd.read_sql(query, connection.get_connection())
    
    if in_json:
        return staff.to_json(orient='records')
    else:
        return staff

def get_facility_job_type(facility_id, job_type_id,  in_json=False):
    ''' Return a list of all staff in the facility'''
    query = """ SELECT a.value, b.dataelementname, b.uid, c.name 
                FROM fact_ihris_datavalue a, dim_ihris_dataelement b, facilities_facility c
                WHERE a.mflcode = c.code 
                    AND a.dataelementid = b.uid
                    AND b.uid = '%s'
                    AND c.id = '%s'"""%( job_type_id,facility_id)
    staff = pd.read_sql(query, connection.get_connection())
    staff['value'] = pd.to_numeric(staff['value'],downcast='float')
    staff = staff.groupby(['dataelementname']).sum()

    if in_json:
        return staff.to_json(orient='records')
    else:
        return staff

def get_country_jobtypes(in_json=False):
    '''return a summaryy of all staff in the country'''
    query = """ SELECT a.value, b.dataelementname as jobtype, b.uid, c.name 
                FROM fact_ihris_datavalue a, dim_ihris_dataelement b, facilities_facility c
                WHERE a.mflcode = c.code 
                    AND a.dataelementid = b.uid"""                
    staff = pd.read_sql(query, connection.get_connection())
    staff['value'] = pd.to_numeric(staff['value'],downcast='float')
    staff = staff.groupby(['jobtype']).sum()

    if in_json:
        return staff.to_json()
    else:
        return staff    

def get_country_county_number_of_staff(in_json=False):
    '''return a summaryy of all staff in the country'''
    query = """ SELECT a.value, b.dataelementname as jobtype, b.uid, c.name , f.name as county
                FROM fact_ihris_datavalue a, dim_ihris_dataelement b, facilities_facility c, common_ward d, common_constituency e, common_county f
                WHERE a.mflcode = c.code 
                    AND a.dataelementid = b.uid
                    AND c.ward_id = d.id 
                    AND d.constituency_id = e.id 
                    AND e.county_id = f.id"""                
    staff = pd.read_sql(query, connection.get_connection())
    staff['value'] = pd.to_numeric(staff['value'],downcast='float')
    staff = staff.groupby(['county']).sum()[['value']]

    if in_json:
        return staff.to_json()
    else:
        return staff    


def get_ward_facility_number_of_staff(ward_id, in_json=False):
    '''return a number of all staff in the ward'''
    query = """ SELECT a.value, b.dataelementname as jobtype, b.uid, c.name, c.ward_id, d.id as id
                FROM fact_ihris_datavalue a, dim_ihris_dataelement b, facilities_facility c, common_ward d
                WHERE a.mflcode = c.code 
                    AND a.dataelementid = b.uid
                    AND c.ward_id = d.id 
                    AND d.id =  '%s' """%(ward_id)
    staff = pd.read_sql(query, connection.get_connection())
    staff['value'] = pd.to_numeric(staff['value'],downcast='float')
    staff = staff.groupby(['name']).sum()[['value']]

    if in_json:
        return staff.to_json()
    else:
        return staff    
