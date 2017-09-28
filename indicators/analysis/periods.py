from django.conf import settings
from common.analysis import connection
import numpy as np
import pandas as pd
from pandas import DataFrame

def get_period_details(period_id, in_json=False):
    ''' return period id details'''
    conn = connection.get_connection()
    all_periods = pd.DataFrame()
    query = "SELECT * FROM dim_dhis_peroid WHERE period_id = %s ;" %(in_json)
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_periods = all_periods.append(chunk)
    
    for column, row in all_periods.iterrows():
        row['year']

#get period ids from year
def get_year_periods(year_id, in_json=False):
    '''return all periods in the year specified '''
    conn = connection.get_connection()
    all_periods = DataFrame()    
    query = "SELECT * FROM dim_dhis_period WHERE yearmonth @@ to_tsquery('%s')" %(year_id)
    for chunk in pd.read_sql(query, con=conn, chunksize=10000):
        all_periods = all_periods.append(chunk)
    
    # all_periods['year'] = int(all_periods['year'.split(' ')[0])
    # all_periods['month'] = int(string.split(' ')[1])
    if in_json:
        return all_periods.to_json(orient='records')
    else:
        return all_periods
    