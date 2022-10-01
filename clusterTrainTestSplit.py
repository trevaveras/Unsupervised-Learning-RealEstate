
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def clusterTrainTestSplit(df, target, c=3):
    
    '''Takes a dataframe with features, a target, and a number of clusters.
    Function returns train test split pairs for each cluster along with a 
    list of their names.
    '''
    
    # original train test split
    X_train, X_test, y_train, y_test = train_test_split(
    df, target, test_size=0.3, random_state=11)
    
    # list clusters by number
    clusters=[]
    for i in range(0,c):
        clusters.append(i)
    
    # X_train
    
    X_trains=[]
    for i in range(0,c):
        X_trains.append('X_train'+str(i))

    X_train_cluster=list(zip(X_trains,clusters)) 

    # loop and append to dictionary
    dataframes1 = {}
    for dxtrain in X_train_cluster:
        dataframes1[dxtrain[0]] = pd.DataFrame(
            X_train.loc[X_train['clusters']==dxtrain[1]].iloc[:,:-1])
 
    # X_test
    
    X_tests=[]
    for i in range(0,c):
        X_tests.append('X_test'+str(i))

    X_test_cluster=list(zip(X_tests,clusters)) 

    # loop and append to dictionary
    dataframes2 = {}
    for dxtest in X_test_cluster:
        dataframes2[dxtest[0]] = pd.DataFrame(
            X_test.loc[X_test['clusters']==dxtest[1]].iloc[:,:-1])

    # y_train
    
    y_trains=[]
    for i in range(0,c):
        y_trains.append('y_train'+str(i))

    y_train_cluster=list(zip(y_trains,clusters)) 

    # loop and append to dictionary
    dataframes3 = {}
    for dytrain in y_train_cluster:
        dataframes3[dytrain[0]] = np.array(
            y_train.loc[X_train.loc[X_train['clusters']==dytrain[1]].index])

            
    # y_test
    
    y_tests=[]
    for i in range(0,c):
        y_tests.append('y_test'+str(i))

    y_test_cluster=list(zip(y_tests,clusters)) 

    # loop and append to dictionary
    dataframes4 = {}
    for dytest in y_test_cluster:
        dataframes4[dytest[0]] = np.array(
            y_test.loc[X_test.loc[X_test['clusters']==dytest[1]].index])

    # concatenate the dictionaries
    dataframes={**dataframes1,**dataframes2,
               **dataframes3,**dataframes4}
    
    # concatenate the list of train test splits by cluster
    dlist=list(zip(X_trains,y_trains,X_tests,y_tests))
    
    X_train=X_train.iloc[:,:-1]
    X_test=X_test.iloc[:,:-1]

    # return dataframes to double check
    return(dataframes, dlist,
          X_train,
          y_train,
          X_test,
          y_test)

    
   