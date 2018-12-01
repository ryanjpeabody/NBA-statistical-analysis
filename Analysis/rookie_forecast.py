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
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def main():
    name = sys.argv[1]
    
    # Read in rookie stat data
    DATA_PATH = '/Users/rjp34/Documents/Github/NBA/Data/'
    ROOKIE_STATS = pd.read_csv(DATA_PATH + 'nba_rookie_per_poss_uncorrected.csv')
    FIELDS =['Player', '3P', '2P', 'FT', 'AST', 'STL', 'BLK', 'TOV']
    STATS = ROOKIE_STATS[FIELDS]
    
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
    distance = dist['distance'].as_matrix()
    
    # Compute moving average
    window = 1
    mva = np.convolve(distance, np.ones((window,))/window, mode='valid')
    
    # Compute first and second derivatives
    d_mva = mva[1:]-mva[:-1]
    dd_mva = d_mva[1:]-d_mva[:-1]
    idx = np.absolute(dd_mva[:500]).argmax()+2

    # Get stats for similar players
    d = {}
    d_stats = {}
    max_length = []
    players = dist.iloc[0:idx+1, 0].tolist()
    for ii in players:
        stats = career_stats(ii)
        d[ii] = stats['stats_change']
        d_stats[ii] = stats['stats']
        max_length.append(len(d[ii]))
        
    # Compute median seasonal changes for stats of interest
    stats_change = pd.DataFrame(columns = d[players[0]].columns)
    for ii in range(0, max(max_length)):
        df = pd.DataFrame(columns = d[players[0]].columns)
        for jj in players:
            try:
                df = df.append(d[jj].iloc[ii,:])
            except:
                continue
        stats_change.loc[len(stats_change),:] = df.median()
            
            
    
    
    trajectory = pd.DataFrame(columns = player_stats.columns[
            player_stats.columns != 'Player'])
        
    
    
    
#------------------------------------------------------------------------------
def career_stats(name):
    DATA_PATH = '/Users/rjp34/Documents/Github/NBA/Data/'
    out_stats = {}
    
    for ii, year in enumerate(range(1979, 2019)):
        df = pd.read_csv(DATA_PATH + 'nba_' + str(year) + '_per_poss.csv')
        df['Player'] = df['Player'].str.replace('*', '')
        if ii == 0:
            player_stats = pd.DataFrame(columns = df.columns)
        player_stats = player_stats.append(df.loc[df.Player == name])
          
    d_stats = player_stats.loc[:, player_stats.dtypes == 'float64'].diff()
    d_stats = d_stats.iloc[1:,:]
    
    out_stats['stats'] = player_stats
    out_stats['stats_change'] = d_stats
    return out_stats
    
    
    
    
    
    

#------------------------------------------------------------------------------
# Boilerplate

if __name__ == '__main__':
    main()