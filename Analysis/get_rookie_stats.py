#!/Users/rjp34/anaconda3/bin/python

# Import packages
import pandas as pd
import numpy as np

path = '../../Data/'

players = []
for ii, year in enumerate(range(1979, 2019)):
    df = pd.read_csv(path + 'nba_' + str(year) + '_per_poss.csv')
    
    # Pull out total games for later
    g = df.G
    
    # Drop data not of interest
    df.drop(['Unnamed: 0', 'Rk', 'Pos', 'Age', 'Tm', 'G', 'GS'], axis = 1, inplace = True)
    
    # Use 1979 to define 1980 rookies as players not playing in 1979
    if year == 1979:
        rookies = pd.DataFrame(columns = df.columns)
        mean_key = pd.DataFrame(columns = df.columns)
        mean_key.drop('Player', axis = 1, inplace = True)
        std_key = mean_key
        old_players = df.Player.values
        
    else:
        
        # Normalize each year's stats as (x - mu)/std. To reverse this, we need to save mu and std for each year
        mean_key = mean_key.append(df.agg(['mean']))
        std_key = std_key.append(df.agg(['std']))
        for jj in df.columns:
            if jj != 'Player':
                df[jj] = (df[jj] - df[jj].mean()) / df[jj].std()
                

        # Rookies defined as players whose names were not previously in players and who played half a season's games
        for jj, name in enumerate(df.Player):
            if name not in players and name not in old_players and g[jj] > np.max(g) // 2:
                players.append(name)
                rookies = rookies.append(df.loc[jj, ])
                rookies.loc[jj, 'Year'] = year
                
rookies.to_csv(path + 'nba_rookie_per_poss.csv')
mean_key.to_csv(path + 'nba_rookie_per_poss_meankey.csv')
std_key.to_csv(path + 'nba_rookie_per_poss_stdkey.csv')