from django.conf import settings
from common.analysis import connection
import numpy as np
import dataelements
import pandas as pd
from pandas import DataFrame
import re
import unicodedata

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

def get_facility_indicator_datavalues(facility_id, indicator_id, period_type, year, in_json=False):    
    indicator = indicators.get_indicator_by_id(indicator_id).loc[0]
    year_periods = periods.get_year_periodtypes(year,period_type)
    facility = orgunits.get_facility_org_units(facility_id).loc[0]
    results = []
    
    #define the pattern for dataelements-categorycombo and extract them
    pattern = "[a-zA-Z0-9]+\.[a-zA-Z0-9]+|[a-zA-Z0-9]+"
    numerator_formula = indicator['numerator']
    new_numerator_formula=''
    denominator_formula = indicator['denominator']
    

    #filter all dataelement only and add to list
    categorycombos_only = re.findall('\.[a-zA-Z0-9]+', indicator['numerator'] + indicator['denominator'])
    categorycombos_only = [ x.encode('ascii','ignore') for x in categorycombos_only]
    #strip off the . 
    categorycombos_only = tuple([re.sub('\.','', x)  for x in categorycombos_only])
    if not categorycombos_only:
        categorycombos_only = """(NULL)"""

    #remove the categoryoptioncombos from the list
    indicator_numerator = re.sub('\.[a-zA-Z0-9]+','', indicator['numerator'] + indicator['denominator'])
    
    #the remaining are dataelements only
    dataelements_only = re.findall('[a-zA-Z0-9]+' , indicator_numerator)
    dataelements_only = tuple([x.encode('ascii','ignore') for x in dataelements_only])
    
    #filter all categoryoption combox and add to list
    for col,period in year_periods.iterrows():
        query = '''
                SELECT a.*, b.uid AS dataelement_uid, c.uid as categoryoptioncombo_uid
                    FROM fact_dhis_datavalue AS a , dim_dhis_dataelement b, dim_dhis_categoryoptioncombo c                    
                    WHERE (  (b.uid  in %s AND c.uid in %s ) OR b.uid  in %s ) 
                    AND a.dataelementid = b.dataelementid
                    AND a.categoryoptioncomboid = c.categoryoptioncomboid
                    AND a.sourceid = %s 
                    AND a.periodid = '%s'
                    LIMIT 1000'''%(str(dataelements_only) , str(categorycombos_only),  str(dataelements_only) ,  facility['organisationunitid'], period['periodid'] )
        values = pd.read_sql(query, connection.get_connection())
        
        
        dataelement_categorycombo_pairs = re.findall('[a-zA-Z0-9]+\.[a-zA-Z0-9]+', numerator_formula)
        if dataelement_categorycombo_pairs:
            for pairs in dataelement_categorycombo_pairs:
                dataelement, categoryoptioncombo =  pairs.split(".") 
                try:
                    value = values.loc[values[(values['dataelement_uid']== dataelement) & (values['categoryoptioncombo_uid']== categoryoptioncombo)].index]['value'].iloc[0]
                except:
                    value = 0                 
                    
                numerator_formula = re.sub("""#{%s.%s}"""%(dataelement, categoryoptioncombo), str(value), numerator_formula)  
                
        temp_numerator_formula = numerator_formula        
        dataelements_only_pairs = re.findall('[a-z,A-Z0-9]{6,}', temp_numerator_formula)
        if dataelements_only_pairs:            
            for pairs in dataelements_only_pairs :   
                
                try:
                    value = values.loc[values[values['dataelement_uid']== pairs].index]['value'].iloc[0]
                except:         
                    value = 0       
                
                numerator_formula = re.sub("""#{%s}"""%(pairs), str(value), numerator_formula)
        numerator_formula = float(eval(numerator_formula))
        
        
        dataelement_categorycombo_pairs = re.findall('[a-zA-Z0-9]+\.[a-zA-Z0-9]+', denominator_formula)
        if dataelement_categorycombo_pairs:
            for pairs in dataelement_categorycombo_pairs:
                dataelement, categoryoptioncombo =  pairs.split(".") 
                try:
                    value = values.loc[values[(values['dataelement_uid']== dataelement) & (values['categoryoptioncombo_uid']== categoryoptioncombo)].index]['value'].iloc[0]
                except:
                    value = 0                 
                    
                denominator_formula = re.sub("""#{%s.%s}"""%(dataelement, categoryoptioncombo), str(value), denominator_formula)  
                
        temp_denominator_formula = denominator_formula        
        dataelements_only_pairs = re.findall('[a-z,A-Z0-9]{6,}', temp_denominator_formula)
        if dataelements_only_pairs:            
            for pairs in dataelements_only_pairs :   
                
                try:
                    value = values.loc[values[values['dataelement_uid']== pairs].index]['value'].iloc[0]
                except:         
                    value = 0
                
                denominator_formula = re.sub("""#{%s}"""%(pairs), str(value), denominator_formula)
        denominator_formula = float(eval(denominator_formula))
        if denominator_formula == 0:
            denominator_formula = 1
        
        

        indicator_value = {
            'indicator_id': indicator['indicatorid'],
            'value': (numerator_formula/denominator_formula),
            'year' : period['year'],
            'month': period['month']
        }
        results.append(indicator_value)
        
        numerator_formula = indicator['numerator']
        denominator_formula = indicator['denominator']
    return results