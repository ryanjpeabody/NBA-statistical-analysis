#!/Users/rjp34/anaconda3/bin/python

# Import packages
import pandas as pd
from sklearn.decomposition import PCA

# Establish path to rookie dataset
path = '/Users/rjp34/Documents/Github/NBA/Data/'

# Read in year-corrected rookie stats
df_work= pd.read_csv(path + 'nba_rookie_per_poss.csv')

# Replace nan values in dataframe with unbiased guess (in this case, 0)
names = df_work['Player']
year = df_work['Year']
df_work.drop(['Unnamed: 0', 'Player', 'Year', 'MP'], axis=1, inplace=True)
df_work.fillna(0, inplace=True)

# Singular value decomposition of rookie stats
X = df_work.as_matrix()
pca = PCA()
pca.fit(X)

print(pca.explained_variance_ratio_)