
from django.conf import settings
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import os
import psycopg2

def get_settings():

    return settings.DW_DATABASE

def get_connection():
    config = settings.DW_DATABASE
    conn_str = "host={} dbname={} user={} password={}".format(
                config['host'], config['database'], 
                config['user'], config['passw'])
    
    try:
        conn = psycopg2.connect(conn_str)
        return conn
    except Exception:
        return Exception.message
