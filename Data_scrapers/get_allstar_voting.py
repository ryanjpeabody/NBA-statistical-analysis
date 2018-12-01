#!/Users/rjp34/anaconda3/bin/python

# Import packages
import pandas as pd
import requests
from bs4 import BeautifulSoup

def allstar_voting(year):

    # Format changes in 2017
    if year <= 2016: 
        
        # Define URL to be scraped
        url = 'https://www.basketball-reference.com/allstar/NBA_' + str(year) + '_voting.html'
     
        # Create BeautifulSoup object
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        table = soup.find_all('table')
    
        df = pd.DataFrame(columns = ['Player', 'Votes', 'Year'])
    
        if year <= 2012:
            num_positions = 3
        else:
            num_positions = 2
        
        for ii in range(2, 2 + mnum_positions*2):
            table_ii = table[ii]
            df_ii = pd.read_html(str(table_ii))
            df_ii = df_ii[0]
            df_ii = df_ii[[1, 2]]
            df_ii.columns = ['Player', 'Votes']
            df_ii['Year'] = year
        
            df = df.append(df_ii)
    else:
        var = ['frontcourt-eastern', 'backcourt-eastern', 'frontcourt-western', 'backcourt-western']
        df = pd.DataFrame(columns = ['Player', 'Votes', 'Year'])
        for ii in var:
        
            url = 'https://www.basketball-reference.com/allstar/NBA_' + str(year) + '_voting-' + ii + '-conference.html'
            
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            table = soup.find_all('table')
            
            tt = table[0]
            df_ii = pd.read_html(str(tt))
            df_ii = df_ii[0]
            df_ii = df_ii.iloc[:, 1:3]
            df_ii.columns = ['Player', 'Votes']
            df_ii['Year'] = year
        
            df = df.append(df_ii)

    return df
        
df_out = pd.DataFrame(columns = ['Player', 'Votes', 'Year'])

for ii in range(1975, 2019):
    if ii != 1999:
        df = allstar_voting(ii)
        df_out = df_out.append(df)
        
    print(str(ii) + ' done!')
      
path_out = '/Users/rjp34/Documents/Github/NBA/Data/'
df_out.to_csv(path_out+'nba_allstar_voting.csv')
    
    
    
    
    
    
    
    
    
    
    
    