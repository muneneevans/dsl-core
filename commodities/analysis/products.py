from common.analysis import connection
from maps.analysis import counties, constituencies, wards
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json

def get_all_products(in_json=False):
    ''' Get all kemsa products '''
    conn = connection.get_connection()
    
    all_products = pd.read_sql('SELECT  DISTINCT(m_product_id) as id, product as name FROM fact_kemsa_order', conn)
    
    if in_json:
        return all_products.to_json(orient='records')
    else:
        return all_products

def get_facility_products(facility_id, in_json=False):
    ''' Return a list of all products that have been ordered by the facility
        returns a dataframe or json string in records orientation'''
    query = """ SELECT a.product as name, a.m_product_id as id, b.id as facility_id, b.name as facility_name
                FROM fact_kemsa_order a, facilities_facility b
                WHERE a.facilitycode = b.code
                AND   b.id = '%s' """%(facility_id)
    facility_products =  pd.read_sql(query,connection.get_connection())
    
    if in_json:
        return  facility_products.to_json(orient='records')
    else:
        return facility_products

def get_facility_year_products(facility_id,year, in_json=False):
    ''' Return a list of all products that have been ordered by the facility
        returns a dataframe or a json stirng on record orientation '''

    query = """ SELECT  a.m_product_id as id, a.product as name , 
                        SUM(a.movementqty) as quantity, SUM(a.qtyordered) as quantity_ordered, 
                        AVG(unitprice) as average_price, date_part('month',  a.dateordered ) as month
                FROM fact_kemsa_order a, facilities_facility b
                WHERE a.facilitycode = b.code
                AND   b.id = '%s' 
                AND date_part('year',  a.dateordered  ) = %s
                GROUP BY a.m_product_id , a.product, a.dateordered"""%(facility_id, year)
    facility_products =  pd.read_sql(query, connection.get_connection())
        
    

    if in_json:
        return facility_products.to_json(orient='records')
    else:
        return facility_products