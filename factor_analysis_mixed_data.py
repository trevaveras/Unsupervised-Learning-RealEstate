# Script to build Factor Analysis of Mixed Data (FAMD) algorithm
# September 12, 2022

# Key sources:

    # Source 1: https://medium.com/analytics-vidhya/the-ultimate-guide-for-clustering-mixed-data-1eefa0b4743b

    # Source 2: https://towardsdatascience.com/famd-how-to-generalize-pca-to-categorical-and-numerical-data-2ddbeb2b9210
    
    
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
import os
from scipy import stats
import math
from sklearn.decomposition import PCA
  
    
# Start with the helper functions:

def calculate_zscore(dataframe, columns):
    '''
    scales columns in dataframe using z-score
    '''
    dataframe = dataframe.copy()
    for col in columns:
        dataframe[col] = (
            dataframe[col] - dataframe[col].mean())/dataframe[col].std(ddof=0)
    
    return dataframe

def one_hot_encode(dataframe, columns):
    '''
    one hot encodes list of columns and
    concatenates them to the original df
    '''

    concat_dataframe = pd.concat([pd.get_dummies(
        dataframe[col], drop_first=True, prefix=col) for col in columns], axis=1)
    one_hot_cols = concat_dataframe.columns

    return concat_dataframe, one_hot_cols

def normalize_column_modality(dataframe, columns):
    '''
    divides each column by the probability μₘ of the modality 
    (number of ones in the column divided by N) only for one hot columns
    '''

    length = len(dataframe)
    for col in columns:

        weight = math.sqrt(sum(dataframe[col])/length)
        dataframe[col] = dataframe[col]/weight

    return dataframe

def center_columns(dataframe, columns):
    '''
    center columns by subtracting the mean value
    '''
    for col in columns:
        dataframe[col] = (dataframe[col] - dataframe[col].mean())

    return dataframe



# Put it all together:


def FAMD_(dataframe, n_components=2):
    
    '''
    Factorial Analysis of Mixed Data (FAMD), 
    which generalizes the Principal Component Analysis (PCA) 
    algorithm to datasets containing numerical and categorical variables
    a) For the numerical variables
    - Standard scale (= get the z-score)

    b) For the categorical variables:
    - Get the one-hot encoded columns
    - Divide each column by the square root of its probability sqrt(μₘ)
    - Center the columns
    c) Apply a PCA algorithm over the table obtained!
    '''

    variable_distances = []

    numeric_cols = dataframe.select_dtypes(include=np.number)
    cat_cols = dataframe.select_dtypes(include='object')

    # numeric process
    normalized_dataframe = calculate_zscore(dataframe, numeric_cols)
    normalized_dataframe = normalized_dataframe[numeric_cols.columns]

    # categorical process
    cat_one_hot_dataframe, one_hot_cols = one_hot_encode(dataframe, cat_cols)
    cat_one_hot_norm_dataframe = normalize_column_modality(
        cat_one_hot_dataframe, one_hot_cols)
    cat_one_hot_norm_center_dataframe = center_columns(
        cat_one_hot_norm_dataframe, one_hot_cols)

    # Merge DataFrames
    processed_dataframe = pd.concat(
        [normalized_dataframe, cat_one_hot_norm_center_dataframe], axis=1)

    # Perform (PCA)
    pca = PCA(n_components=n_components)
    principalComponents = pca.fit_transform(processed_dataframe)
    variance_explained=pca.explained_variance_ratio_

    return principalComponents,variance_explained,processed_dataframe




