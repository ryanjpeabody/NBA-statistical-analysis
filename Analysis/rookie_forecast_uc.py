#!/Users/rjp34/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 11:33:54 2018

@author: rjp34
"""
#------------------------------------------------------------------------------
# Package imports

import sys
import pandas as pd
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def main():
    name = sys.argv[1]
    
    # Read in rookie stat data
    DATA_PATH = '/Users/rjp34/Documents/Github/NBA/Data/'
    ROOKIE_STATS = pd.read_csv(DATA_PATH + 'nba_rookie_per_poss_uncorrected.csv')
    STATS = ROOKIE_STATS[['Player', '3P', '2P', 'FT', 'ORB', 'DRB', 'AST',
                          'STL', 'BLK', 'TOV']]
    
    # Get input player stats and delete them from the rookie stat file
    I = STATS['Player'] == name
    if not any(I):
        sys.exit('No match for entered name')
    player_stats = STATS.loc[I]
    STATS = STATS.loc[~I]
    
    # Find euclidean distance to input player statline
    dist = pd.DataFrame(data = None, columns = player_stats.columns)
    dist['Player'] = STATS['Player']
    for ii in player_stats.columns:
        if ii != 'Player':
            dist[ii] = (STATS[ii] - float(player_stats[ii]))**2
    dist['distance'] = dist.loc[:, dist.columns != 'Player'].sum(axis=1)
    dist = dist[['Player', 'distance']]
    dist.sort_values(by = 'distance', inplace = True)
    
    print(dist.head())
    plt.plot([x for x in range(1,501)], dist.iloc[:500, 1])
    plt.show()
        
     
           
    
    
    
    
    
    
    
    

#------------------------------------------------------------------------------
# Boilerplate

if __name__ == '__main__':
    main()