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