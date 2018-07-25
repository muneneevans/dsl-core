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
    '''returns an orgunit with the code matching that of the facility
        retruns a dataframe object or json with record orientation'''
    conn = connection.get_connection()        
    query = ''' SELECT  a.organisationunitid, a.code, b.name
                FROM dim_dhis_organisationunit a , facilities_facility b
                WHERE a.code = CAST(b.code as VarChar) AND b.id = '%s' ''' %(facility_id)
    
    facility_orgunit = pd.read_sql(query,conn)
    
    if in_json:
        return facility_orgunit.to_json(orient='records')
    else:
        return facility_orgunit