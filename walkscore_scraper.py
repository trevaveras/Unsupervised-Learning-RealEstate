
def walkscore_scraper():

    '''Scrapes zip code level walk scores in Georgia and returns dataframe with zip codes,
    and matching walk scores, which can be merged to listings data.'''

    from bs4 import BeautifulSoup
    import requests
    import numpy as np
    import time
    import re
    import pandas as pd
    import time


    headers={'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    # read the listings file
    df=pd.read_csv(
        './data/GA_LISTINGS_SALES_V2.csv')

    # create a unique zip codes column
    df=pd.DataFrame(df.zip.unique(), columns=['zip'])

    # create a column with the base url
    df['site']='https://www.walkscore.com/score/'

    # join base url and formatted address 
    df['url']=df['site'].str.cat(df['zip'], sep='')

    #scrape walk scores
    walkscores=[]
    times=[]
    for url in df['url']:
            timestart=time.time() 


            response=requests.get(url,headers=headers)
            text=BeautifulSoup(response.text, 'html.parser')

    #         if response.status_code != 200:
    #             raise Exception(f'The status code is not 200! It is {response.status_code}.')   

            try:
                #get title
                score = text.find('div',
                                  {'class':'block-header-badge score-info-link'}).find('img').get('src')

            except:
                score=np.nan



            #store info in dictionary
            walkscores.append(score)
            #time.sleep(1)
            timestop=time.time() 
            times.append(timestart-timestop)

    scores=[]
    for i in range(0,len(walkscores)):
        try:
            scores.append(walkscores[i].split('/')[-1].split('.')[0])
        except:
            scores.append(np.NaN)


    # convert to df
    scoresdf=pd.DataFrame(scores, columns=['score'])
    # convert dtype to float
    scoresdf['score']=scoresdf['score'].astype('float')
    # impute missing row
    scoresdf['score'].fillna(value=scoresdf['score'].mean(), inplace=True)


    zipwalkscores=df.join(scoresdf)

    zipwalkscores=zipwalkscores.loc[zipwalkscores['zip']!='00000']
    zipwalkscores=zipwalkscores.loc[zipwalkscores['zip']!='None']
    zipwalkscores=zipwalkscores.filter(['zip','score']).reset_index(drop=True)
    #rename walking score column
    zipwalkscores=zipwalkscores.rename(columns={'score':'walkscore'})
    
    # convert walks zip to str
    zipwalkscores['zip']=zipwalkscores['zip'].astype(str)
    #export to CSV
    zipwalkscores.to_csv(
        './data/zipwalkscores.csv',
                        index=False)
    #return dataframe
    return(zipwalkscores)