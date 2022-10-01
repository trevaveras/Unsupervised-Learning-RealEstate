from read_data_files import *
from grocery_scraper import *
from so_fresh_so_clean import *
from walkscore_scraper import *
from distance_calculator import *


def mycompiler():
    
    '''Read data files, calculate distances, merge zip-level features. Return clean, complete df.
    '''
    


    # read data
    listings=df_cleaner()
    groceries=grocery_scraper()
    banks=banks_df()
    schools=schools_df()
    crime=crime_df()

    # this one takes 4-5 minutes
        # SKIP AND JUST READ THE CSV INSTEAD to save time
    #walkscores=walkscore_scraper()
    walkscores=pd.read_csv(
        './data/zipwalkscores.csv')
    #convert zip to string for mergine
    walkscores['zip']=walkscores['zip'].astype(str)

    # get distances
    listings=min_dist('grocer_dist',groceries, listings)
    listings=min_dist('bank_dist',banks, listings)
    listings=min_dist('school_dist',schools, listings)

    # merge listings and zip code data
    listings=pd.merge(listings,walkscores,on='zip', how='left').reset_index(drop=True)
    # merge listings and crime rates
    listings=pd.merge(listings,crime,on='zip', how='left').reset_index(drop=True)
    # impute missing crime rates due to merge
    for i in listings.filter(regex='rate$',axis=1):
        listings[i].fillna(listings[i].mean(),inplace=True)

    # return final dataframe
    return(listings)

