

# import library
import pandas as pd
import csv
import seaborn as sns
import numpy as np

    
# 1. Read banks data
    
def banks_df():
    
    '''Read and clean banks data.''' 

    # open the file
    data=open('./data/GA_2022_Data.csv')
    # create csv reader
    reader=csv.reader(data)
    # extract column names
    header = []
    header = next(reader)
    # extract row data
    rows = []
    for row in reader:
            rows.append(row)
    # put it together in a dataframe
    banks=pd.DataFrame(rows, columns=(header))
    # convert columns to lowercase
    banks.columns=banks.columns.str.lower()


    # filter columns, drop na
    banks=banks.filter(['sims_latitude','sims_longitude','addresbr']).dropna()

    #rename columns
    banks=banks.rename(columns = {'sims_latitude':'lat','sims_longitude':'lon',
                           'addresbr':'banks'})# convert to float
    #convert to floats
    banks['lat']=banks['lat'].astype(float)
    banks['lon']=banks['lon'].astype(float)

    return(banks)


# 2. Read schools data

def schools_df():

    '''Reads in schools data, concatenates files, cleans data.
    '''

    elementary=pd.read_csv(
        './data/elementary_schools.csv')
    middle=pd.read_csv(
        './data/middle_schools.csv')
    highschool=pd.read_csv(
        './data/high_schools.csv')

    # append schools files
    schools=pd.concat([elementary,middle,highschool])

    #rename the longitude column
    schools=schools.rename(columns={'long':'lon'})

    # remove duplicates
    schools=schools.drop_duplicates(subset=['address'])

    # keep only what we need
    schools=schools[['lat','lon','address']].reset_index(drop=True)

    return(schools)


# 3. Read crime data

def crime_df():
    ''' Reads and cleans crime data for zip code level merge. 
    '''

    crime=pd.read_csv(
        './data/crime_rating_zipcode.csv')

    # keep only the rates and zip code columns
    crime=(crime.filter(regex='rate$',axis=1)).join((crime['census_zcta5_geoid']))

    # rename census zcta5 to zip
    crime=crime.rename(columns={'census_zcta5_geoid':'zip'})

    # convert data type to prep for join
    crime['zip']=crime['zip'].astype(str)
    
    # impute missing crime rate data
    for i in crime.filter(regex='rate$',axis=1):
        crime[i].fillna(crime[i].mean(),inplace=True)

    return(crime)


