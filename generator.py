import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from extract_playlist_features import extract_playlist_features

playlist_url= "https://open.spotify.com/playlist/0HgyP1EIfHA4m7apeARZJW?si=ce640ab3c2164acd"
playlist_df = extract_playlist_features(playlist_url)

# all the dummies from the big dataset
all_dummies = ['A Major', 'A Minor',
    'Ab Major', 'Ab Minor', 'B Major', 'B Minor', 'Bb Major', 'Bb Minor',
    'C Major', 'C Minor', 'D Major', 'D Minor', 'Db Major', 'Db Minor',
    'E Major', 'E Minor', 'Eb Major', 'Eb Minor', 'F Major', 'F Minor',
    'F# Major', 'F# Minor', 'G Major', 'G Minor', '1920s', '1930s', '1940s',
    '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']

# make dummies for key/mode and decades
key_dummies = pd.get_dummies(playlist_df['key_mode'])
decade_dummies = pd.get_dummies(playlist_df['decade'])
dummies = pd.concat([ key_dummies, decade_dummies], axis=1)

# check which dummies weren't created - we need to add these in as zeros so the dataframes have the same shape
playlist_df = pd.concat([playlist_df, key_dummies, decade_dummies], axis=1)
zeroes = list(set(all_dummies) - set(dummies.columns))

# add those dummies in as zeroes
for col in zeroes:
    playlist_df[col] = 0

# drop first column for dummies
playlist_df.drop(['A Major', '1920s'],axis=1, inplace=True)


labels_df = pd.read_csv('data-historical.csv',index_col=[0])

# drop unnecesary features
labels_df.drop(['key_mode', 'decade', 'modes', 'letter_keys',  'year', 
         'release_date', 'mode', 'loudness', 'key', 'id', 'explicit', 
         'tempo', 'duration_ms', 'speechiness', 'popularity' ], axis=1, inplace=True)



