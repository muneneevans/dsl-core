from common.analysis import connection
from maps.analysis import counties, constituencies, wards
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json

def get_all_products(in_json=False):
    ''' Get all kemsa products '''
    conn = connection.get_connection()
    
    all_products = pd.read_sql('SELECT  DISTINCT(m_product_id), product FROM fact_kemsa_order', conn)
    
    if in_json:
        return all_products.to_json(orient='records')
    else:
        return all_products