from django.conf import settings
from common.analysis import connection
import numpy as np
import dataelements
import pandas as pd
from pandas import DataFrame
import re

from . import dataelements, indicators, periods, category_option_combos, orgunits

def get_all_datavalues(in_json=False):
    '''return all datavalues in the datase'''
    conn = connection.get_connection()
    all_datavalues = DataFrame()

    for chunk in pd.read_sql('SELECT * FROM fact_dhis_datavalue LIMIT 50000', con=conn, chunksize=1000):
        all_datavalues = all_datavalues.append(chunk)
    
    if in_json:
        return all_datavalues.to_json(orient='records')
    else:
        return all_datavalues

def get_dataelement_datavalues(dataelement_id, in_json=False):
    '''return all data values in a dataelement'''
    # conn = connection.get_connection()
    all_datavalues = get_all_datavalues()

    dataelement = dataelements.get_dataelement_by_id(dataelement_id)

    dataelement_datavalues = pd.merge(all_datavalues, dataelement, on='dataelementid')

    dataelement_datavalues = dataelement_datavalues[['periodid','sourceid','categoryoptioncomboid','attributeoptioncomboid','value']]
    if in_json:
        return dataelement_datavalues.to_json(orient='records')
    else:
        return dataelement_datavalues

def get_facility_dataelement_datavalues(dataelement_id, source_id, period_id, category_combo_id=None, in_json=False):
    conn = connection.get_connection()
    all_datavalues = DataFrame()
    
    if category_combo_id:
        query = ''' SELECT a.* 
                    FROM fact_dhis_datavalue a , dim_dhis_dataelement b
                    WHERE a.dataelementid = b.dataelementid
                    AND b.uid = '%s' 
                    AND a.sourceid = %s 
                    AND a.periodid = '%s'
                    AND a.categoryoptioncomboid = '%s' ''' %(dataelement_id, source_id, period_id, category_combo_id)
    else:
        query = ''' SELECT a.* 
                FROM fact_dhis_datavalue a , dim_dhis_dataelement b
                WHERE a.dataelementid = b.dataelementid
                AND b.uid = '%s' 
                AND a.sourceid = %s 
                AND a.periodid = '%s'; ''' %(dataelement_id, source_id, period_id)
    all_datavalues = pd.read_sql(query, con=conn )       
    
    if in_json:
        return all_datavalues.to_json(orient='records')
    else:
        return all_datavalues


def get_period_datavalues(facility,period, indicator, numerator_dataelements, denominator_dataelements ,results, index):
    numerator = indicator['numerator'] 
    
    #iterate through dataelements 
    for datelement_category_combo in numerator_dataelements:           
        #extract the data element by searching for datalement. and replace with the id
        datelement= None

        # check if the dataelement has a category combo
        combo = re.findall("\.[a-zA-Z0-9]+", datelement_category_combo)

        if combo:
            #remove . in category combo expression and get uid
            combo = re.sub('\.','', combo[0])
            combo_uid = category_option_combos.get_category_option_combo_by_uid(combo).loc[0]['categoryoptioncomboid']

            dataelement = re.sub('\.','' , re.findall("[a-zA-Z0-9]+\.", datelement_category_combo)[0]) 
            
        else:
            combo_uid = None
            dataelement = re.findall("[a-zA-Z0-9]+", datelement_category_combo)[0]

        value = get_facility_dataelement_datavalues(dataelement, facility['organisationunitid'], period['periodid'], combo_uid)

        if value.empty:            
            numerator = re.sub( "#{" + datelement_category_combo +"}" ,'0',numerator)                
        else:
            numerator = re.sub("#{" + datelement_category_combo +"}" ,value.loc[0]['value'],numerator)                
    numerator = float(eval(numerator))


    denominator = indicator['denominator']
    for datelement_category_combo in denominator_dataelements:                       
        datelement = None

        combo = re.findall("\.[a-zA-Z0-9]+", datelement_category_combo)
        if combo:
            combo = re.sub('\.','', combo[0])
            combo_uid = category_option_combos.get_category_option_combo_by_uid(combo).loc[0]['categoryoptioncomboid']
            dataelement = re.sub('\.','' , re.findall("[a-zA-Z0-9]+\.", datelement_category_combo)[0]) 
        else:
            combo_uid = None
            dataelement = re.findall("[a-zA-Z0-9]+", datelement_category_combo)[0]

        value = get_facility_dataelement_datavalues(dataelement, facility['organisationunitid'], period['periodid'], combo_uid)
        if value.empty:      
            denominator = re.sub( "#{" + datelement_category_combo +"}" ,'1',denominator)                
        else:
            denominator = re.sub("#{" + datelement_category_combo +"}" ,value.loc[0]['value'],denominator)                
    denominator =  float(eval(denominator))
    indicator_value = {
        'indicator_id': indicator['indicatorid'],
        'value': (numerator/denominator),
        'year' : period['year'],
        'month': period['month']
    }

    results.append(indicator_value)
        
    return results


def get_facility_indicator_datavalues(facility_id, indicator_id, period_type, year , in_json=False):
    from threading import Thread
    
    conn = connection.get_connection()
    indicator = indicators.get_indicator_by_id(indicator_id).loc[0]
    year_periods = periods.get_year_periodtypes(year,period_type)
    facility = orgunits.get_facility_org_units(facility_id).loc[0]
    
    threads = [None] * len(year_periods.index)
    results = []
    
    #define the pattern for dataelements-categorycombo and extract them
    pattern = "[a-zA-Z0-9]+\.[a-zA-Z0-9]+|[a-zA-Z0-9]+"
    numerator_dataelements = re.findall(pattern,indicator['numerator'])
    denominator_dataelements = re.findall(pattern,indicator['denominator'])

    
    #iterate through all periods
    for col, period in year_periods.iterrows():
        threads[col] = Thread(target= get_period_datavalues, args=(facility, period, indicator, numerator_dataelements, denominator_dataelements, results, col))
        threads[col].start()

    for i in range(len(threads)):
        threads[i].join()
    
    return results