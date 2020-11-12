import env
import pandas as pd
import numpy as np
import os
import requests

########## Acquire ##########

def get_data():
    colnames=['date','time','page_viewed','user_id','cohort_id','ip'] #labeling column names

    #bringing in the txt file
    df = pd.read_csv('anonymized-curriculum-access.txt',  #file being brought in
                    engine='python',
                    header=None,
                    index_col=False,
                    names=colnames, #will be labeling the the columns the names above
                    sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                    na_values='"-"',
                    usecols=[0,1,2,3,4,5]) #only using these specified columns
    df.replace('/', 'home', inplace=True)

    return df


def df_cohort():
    colnames=['cohort_id','name','start_date','end_date','program_id']
    df_cohort = pd.read_csv('cohorts.csv',
                       names=colnames, 
                       skiprows=1,
                       usecols=[0,1,2,3,4])
    
    return df_cohort


########## Prepare ##########

def null_df(df):
    df2 = df[df.cohort_id.isna()]
    df2.cohort_id.fillna(0, inplace=True)
    return df2


########## Explore ##########

def ip_locator(ips):
    ips_df = []

    counter = 0

    for ip in ips:

        url = "https://free-geo-ip.p.rapidapi.com/json/" + ip

        headers = {
            'x-rapidapi-key': env.rapidapi_key,
            'x-rapidapi-host': "free-geo-ip.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers)
        data = response.json()
    
        ips_df.append(data)

    return ips_df