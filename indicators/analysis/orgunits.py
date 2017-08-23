from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame
from facilities.analysis import facilities



#get all organization units
def get_organization_units(in_json=False):
    '''returns a list of all organization units'''
    conn = connection.get_connection()
    all_orgunits = pd.DataFrame()
    for chunk in pd.read_sql('SELECT * FROM dim_dhis_organisationunit', con=conn, chunksize=10000):
        all_orgunits = all_orgunits.append(chunk)
    
    if in_json:
        return all_orgunits.to_json(orient='records')
    else:
        return all_orgunits


#get a orgunit matching a facility
def get_facility_org_units(facility_id, in_json=False):
    '''returns an orgunit with the code matching that of the facility'''
    #get the facility 
    facility = facilities.get_facility_by_id(facility_id)
    facility['code'] = facility['code'].astype(str)
    
    #get all org units
    all_orgunits = get_organization_units()
    all_orgunits['code'] = all_orgunits['code'].astype(str)
    facility_orgunits = pd.merge(all_orgunits, facility, on='code')
    
    facility_orgunits = facility_orgunits.head(1)

    if in_json:
        return facility_orgunits.to_json(orient='records')
    else:
        return facility_orgunits