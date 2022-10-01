


import os
import pandas as pd
import numpy as np


def mypca(df,n_components=3):
    '''Performs principal components analysis on cleaned listings dataframe,
    returns explained variance, loading vectors, principal components.
    '''
    
    # drop price (our target for supervised learning later on)
    df=df.drop(['price'], axis=1)
    
    # identify list of numerical features
        # start in position 2 to ignore lat long
    numers=[]
    for col in df.columns[2:]:
        if df[col].dtype==('float64') or df[col].dtype==('int64'):
            numers.append(col)

    # assign numeric features to df; do not subset only 1 crime rate
        # detailed crime rate data is key to producing clusters
    df=df[numers]#.iloc[:,:9]

    # import PCA libraries
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    # create PCA object
    pca = PCA(n_components=n_components)


    # scale numeric data for PCA
    scaler=StandardScaler()
    scaler.fit(df)
    scaled_df=scaler.transform(df)

    # fit_tranform PCA to data
    pca_components_data=pca.fit_transform(scaled_df)

    # save explained variance
    variance_explained=pca.explained_variance_ratio_

    c_list=[]
    for i in range(0,(pca.components_.shape[0])):
        c_list.append('pc%d' %(i+1))

    # examine the loading vectors to assess correlations between components and features
    loadings = pd.DataFrame(
        pca.components_.T, columns=c_list, index=df.columns)


    return(variance_explained, loadings, pca_components_data)

