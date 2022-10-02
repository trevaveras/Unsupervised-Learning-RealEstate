train[col].dtype=='int64'

def grocery_scraper():
    
    '''Scrapes Whole Foods and Trader Joe's listings from Superpages classifieds,
    returns dataframe with geocoded quality grocers, including lat/long.'''



    from bs4 import BeautifulSoup
    import requests
    import numpy as np
    import time
    import re
    import pandas as pd
    headers={'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


    # PART I: Whole Foods

    # create response object
    response = requests.get('https://www.superpages.com/search?search_terms=whole+foods+market&geo_location_terms=GA', headers = headers)

    # pull the text
    text = BeautifulSoup(response.content,'html.parser')

    # get listing titles info
    titles=text.find_all('a', {'class':'business-name'})

    # get store names
    names=list([tag.find('span').string for tag in titles])

    # get address info
    locationtags=text.find_all('div', attrs={'class':'street-address'})

    # get addresses
    addresses=list([tag.string for tag in locationtags])


    # zip up store names and addresses
    wfds=pd.DataFrame((list(zip(names,addresses))), columns=['store','address'])


    # PART II: Trader Joe's

    # create response object

    response = requests.get(
        'https://www.superpages.com/search?search_terms=trader+joe%27s&geo_location_terms=GA',
        headers = headers)

    # pull the text
    text2 = BeautifulSoup(response.content,'html.parser')

    # get listing titles info
    titles2=text2.find_all('a', {'class':'business-name'})

    # get store names
    names2=list([tag.find('span').string for tag in titles2])

    # get address info
    locationtags2=text2.find_all('div', attrs={'class':'street-address'})

    # get addresses
    addresses2=list([tag.string for tag in locationtags2])

    # zip up store names and addresses
    tjs=pd.DataFrame((list(zip(names2,addresses2))), columns=['store','address'])
    # filter non-trader joe's
    tjs=tjs.loc[tjs['store']=="Trader Joe's"]
    # filter duplicate (spotted manually)
    tjs=tjs[:-1]

    # append trader joe's and whole foods markets
    qual_groc=pd.concat([wfds,tjs]).reset_index(drop=True)

    # PART III: Geocode the data using Google Maps API

    base_url='https://maps.googleapis.com/maps/api/geocode/json?'

    response=[]
    for i in qual_groc.address:
        response.append(requests.get(base_url,
                                     params={
                                    # 'key':'enter your google api key here',
                                     'address':i}).json())

    lat=[]
    long=[]
    for i in range(0,len(response)):
        lat.append(response[i]['results'][0]['geometry']['location']['lat'])
        long.append(response[i]['results'][0]['geometry']['location']['lng'])


    # zip and save lat long into dataframe
    coords=pd.DataFrame((list(zip(lat,long))), columns=['lat','long'])

    # merge w grocers info dataframe
    grocers=pd.concat([qual_groc,coords], axis=1)
    
    #rename the longitude column
    grocers=grocers.rename(columns={'long':'lon'})

    return(grocers)



