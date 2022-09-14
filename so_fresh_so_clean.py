# Cleaning Script for HaystacksAI project
# September 12, 2022


def df_cleaner(dataframe):
    '''Returns a clean dataframe with no missing data or outliers,
    ready for further analysis steps.'''

    # import libraries
    import pandas as pd
    import numpy as np
    import seaborn as sns
    #%matplotlib inline
    import matplotlib
    from matplotlib import pyplot as plt
    import os
    from scipy import stats
    import math






    # drop first column
    df=dataframe.iloc[:,1:]

    # strip property type from details feature column
    df.details=df.details.str.split(',', expand=True)[[0]]

    # include only detached properties
    df=df.loc[df['details']=='Detached']

    # drop properties with zero square footage
    df=df.loc[df['square_footage']!=0]

    # reset index 
    df=df.reset_index(drop=True)

    # identify categorical data (ensure it is set to object type):

        #city
        #county_name
        #details (extract house type)
        #special features (probably categorical, convert to object type)
    df['special_features'] = df['special_features'].astype(object)
        #transaction_type ( this needs to be converted to object))
    df['transaction_type'] = df['transaction_type'].astype(object)
        #listing_status (convert to object)
    df['listing_status'] = df['listing_status'].astype(object)
        #listing_special_features (covert to object)
    df['listing_special_features'] = df['listing_special_features'].astype(object)
        #census_state_name 
        #census_county_name
        #zip 

    # drop unit count, baths_half, columns with a majority null values
    df=df.drop(['unit_count','baths_half'], axis=1)
    
    #drop additional rows to focus on more useful data
    df=df.drop(['lot_size'], axis=1)
    df=df.loc[df['square_footage']>100]
    df=df.loc[df['price']>20000]

    # impute missing observations

    # beds
    df.beds.fillna(value=df.beds.mean(), inplace=True)
    # baths_full
    df.baths_full.fillna(value=df.baths_full.mean(), inplace=True)
    # square_footage (impute by avg by beds)
    df.square_footage.fillna(value=df.square_footage.mean(), inplace=True)
    # lot_size
    df.lot_size.fillna(value=df.lot_size.mean(), inplace=True)
    # year_built
    df.year_built.fillna(value=df.year_built.mean(), inplace=True)

    # save a list of categorical cols just in case
    cats=[]
    for col in df.columns:
        if df[col].dtype=='object':
            cats.append(col)

    # save a list of numerical cols just in case

    numers=[]
    for col in df.columns:
        if df[col].dtype==('float64') or df[col].dtype==('int64'):
            numers.append(col)


    # remove outliers

    # convert outliers to NaN, which we can then easily drop

    for col in df.columns:
        if df[col].dtype==('float64') or df[col].dtype==('int64'):
            z = np.abs(stats.zscore(df[[col]]))
            df[col]=df[col][(z<3).all(axis=1)]  

    # drop NaN
    df=df.dropna()

    '''for now we won't label encode,
    but if we need to, uncomment the lines here below'''

    # from sklearn.preprocessing import LabelEncoder
    # lencoder = LabelEncoder()


    # for col in df.columns:
    #     if df[col].dtype=='object':
    #         df[col]=lencoder.fit_transform(df[col])


    '''for now there is no need to recode label encoded categorical data as object,
    but if we need to we can uncomment  this out here below'''

    # for col in df.columns:
    #     if col in cats:
    #         df[col]=df[col].astype(object)
    
    return df.reset_index(drop=True)

