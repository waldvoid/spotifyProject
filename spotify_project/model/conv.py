import pandas as pd

data = pd.read_csv('model/data/data.csv')
data = data.rename(columns={'name': 'track_name', 'artists': 'artists_names', 'id': 'track_id', 'artist_names': 'artists_names'})
data['id'] = range(len(data))
data['album_release_date'] = 0
data.to_excel('model/data/data.xlsx', index=False)
data = pd.read_excel('model/data/data.xlsx')
