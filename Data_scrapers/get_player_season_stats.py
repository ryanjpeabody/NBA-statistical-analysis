#!/Users/rjp34/anaconda3/bin/python

# Import packages
import pandas as pd
import requests
from bs4 import BeautifulSoup

def player_season_stats(year):

    # Define URL to be scraped
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_poss.html'
    
    # Define CSV name to be written
    file_out = 'nba_' + str(year) + '_per_poss.csv'
    
    # Create BeautifulSoup object
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    table = soup.find_all('table')[0]
    
    # Read object in as DataFrame
    df = pd.read_html(str(table))
    df = df[0]
    
    # Drop unnamed column (buffer column from basketball-reference)
    df = df.drop('Unnamed: 29', axis = 1)
    
    # Drop buffer rows
    df = df[df.Rk != 'Rk']
    
    # Write to CSV
    df.to_csv(file_out)
    
for ii in range(1974, 2017):
    player_season_stats(ii)
    print(str(ii) + ' done!')