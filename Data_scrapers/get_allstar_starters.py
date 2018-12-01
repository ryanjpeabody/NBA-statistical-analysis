#!/Users/rjp34/anaconda3/bin/python

# Import packages
import pandas as pd
import requests
from bs4 import BeautifulSoup

def allstar_starters(year):

    # Define URL to be scraped
    url = 'https://www.basketball-reference.com/allstar/NBA_' + str(year) + '.html'
    
    # Define CSV name to be written
    file_out = 'nba_' + str(year) + '_allstar_starters.csv'
    
    # We need to read out both East and West starters
    # West starters are in [1], East in [2]

    # Create BeautifulSoup object
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    
    # West
    table = soup.find_all('table')[1]
    west_df = pd.read_html(str(table))
    west_df = west_df[0][0:4]
    west_df.columns = list(zip(*west_df.columns))[1]

    # East
    table = soup.find_all('table')[2]
    east_df = pd.read_html(str(table))
    east_df = east_df[0][0:4]
    east_df.columns = list(zip(*east_df.columns))[1]
    
    # Concatenate and add year
    df_local = pd.concat([west_df, east_df])
    df_local['Year'] = year
    
    return df_local
    
for ii in range(1974, 2018):
    if ii != 1999: # No 1999 all-star game
        print(str(ii) + ' done!')
    
        df_local = allstar_starters(ii)
    
        if ii == 1974:
            df_out = pd.DataFrame(columns = df_local.columns)
    
        df_out = df_out.append(df_local)
    
path_out = '../../Data/'
df_out.to_csv(path_out+'nba_allstar_starters.csv')
    
    
    
    
    
    
    
    
    
    
    
    