def extract_playlist_features(user_playlist_url, sp):
    import pandas as pd
    import numpy as np
    from sklearn import set_config
    set_config(print_changed_only=False, display=None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    import warnings
    warnings.filterwarnings('ignore')


    # Playlist ID'yi URL'den çıkar
    playlist_id = user_playlist_url.split('/')[-1].split('?')[0]

    # Playlistteki şarkıları çek
    results = sp.playlist(playlist_id)

    # Şarkı bilgilerini sakla
    song_ids = []
    release_dates = []
    popularities = []
    for item in results['tracks']['items']:
        track = item['track']
        song_ids.append(track['id'])
        release_dates.append(track['album']['release_date'])
        popularities.append(track['popularity'])

    # Şarkı özelliklerini çek
    attributes = sp.audio_features(tracks=song_ids)

    # Şarkı enerjisi ve çıkış tarihlerini özelliklere ekle
    for i in range(len(attributes)):
        attributes[i]['release_date'] = release_dates[i]
        attributes[i]['popularity'] = popularities[i]


    # Tüm özelliklerden bir DataFrame oluştur
    playlist_df = pd.DataFrame(attributes)

    # Gereksiz feature'ları sil
    playlist_df.drop(['type', 'id', 'track_href', 'analysis_url', 'time_signature'], axis=1, inplace=True)

    # release_date'i datetime'a çevir
    playlist_df['release_date'] = pd.to_datetime(playlist_df['release_date'], format='ISO8601')

    # yıl sütunu oluştur
    playlist_df['year'] = playlist_df['release_date'].dt.year

    # decade sütunu oluştur
    playlist_df['decade'] = playlist_df['year'].apply(lambda x: str(x)[:3]+'0')

    # key ve mode sütunlarını seslere çevir
    keys = {0:'C', 1:'Db',2:'D',3:'Eb',4:'E',5:'F',6:'F#',7:'G',8:'Ab',9:'A',10:'Bb',11:'B'}
    modes = {0:'Minor',1:'Major'}

    # yeni sütunları ekle
    playlist_df['letter_keys'] = playlist_df['key'].map(keys)
    playlist_df['modes'] = playlist_df['mode'].map(modes)

    # key ve mode sütunlarını birleştir yeni bir sütun oluştur
    playlist_df['key_mode'] = playlist_df['letter_keys'] + " " + playlist_df['modes']

    # eşik değer ortalamasından 5 aşağı - yukarı standart sapması uygula
    numerical_cols = playlist_df.select_dtypes(include=[np.number]).columns
    for feat in numerical_cols:
        abv_5_std = playlist_df[feat].mean()+ 5* playlist_df[feat].std()
        below_5_std = playlist_df[feat].mean()- 5* playlist_df[feat].std()
        conditions = [playlist_df[feat]>abv_5_std, playlist_df[feat]<below_5_std]
        choices = [abv_5_std, below_5_std]
        playlist_df[feat] = np.select(conditions, choices, playlist_df[feat])


    # 0-1 arasında standartlaştır
    playlist_df['scaled_speech'] = (playlist_df['speechiness'] - min(playlist_df['speechiness'])) / (max(playlist_df['speechiness']) - min(playlist_df['speechiness']))
    playlist_df['scaled_duration'] = (playlist_df['duration_ms'] - min(playlist_df['duration_ms'])) / (max(playlist_df['duration_ms']) - min(playlist_df['duration_ms']))
    playlist_df['scaled_loudness'] = (playlist_df['loudness'] - min(playlist_df['loudness'])) / (max(playlist_df['loudness']) - min(playlist_df['loudness']))
    playlist_df['scaled_instrumentalness'] = (playlist_df['instrumentalness'] - min(playlist_df['instrumentalness'])) / (max(playlist_df['instrumentalness']) - min(playlist_df['instrumentalness']))
    playlist_df['scaled_tempo'] = (playlist_df['tempo'] - min(playlist_df['tempo'])) / (max(playlist_df['tempo']) - min(playlist_df['tempo']))
    playlist_df['scaled_energy'] = (playlist_df['energy'] - min(playlist_df['energy'])) / (max(playlist_df['energy']) - min(playlist_df['energy']))
    playlist_df['scaled_danceability'] = (playlist_df['danceability'] - min(playlist_df['danceability'])) / (max(playlist_df['danceability']) - min(playlist_df['danceability']))
    playlist_df['scaled_popularity'] = (playlist_df['popularity'] - min(playlist_df['popularity'])) / (max(playlist_df['popularity']) - min(playlist_df['popularity']))

    
    desired_columns = ['uri', 'instrumentalness', 'popularity','danceability', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'energy', 'release_date', 'year', 'decade', 'letter_keys', 'modes', 'key_mode', 'scaled_speech', 'scaled_instrumentalness', 'scaled_duration', 'scaled_loudness', 'scaled_tempo', 'scaled_energy', 'scaled_danceability', 'scaled_popularity']

    # Sütunları yeniden sırala
    playlist_df = playlist_df[desired_columns]
    # Sıralama ID'si ekle
    playlist_df.reset_index(inplace=True)
    playlist_df.rename(columns={'index': 'id'}, inplace=True)
    
    key_dummies = pd.get_dummies(playlist_df['key_mode'], drop_first=True)
    decade_dummies = pd.get_dummies(playlist_df['decade'], drop_first=False)

    playlist_df = pd.concat([playlist_df, key_dummies, decade_dummies], axis=1)
    
    # 1980's'den 2020's'e kadar olan decadeleri ekle
    decades = ['1960','1970','1980', '1990', '2000', '2010', '2020']
    for decade in decades:
        if decade not in playlist_df.columns:
            playlist_df[decade] = False

    desired_columns = ['id', 'uri', 'popularity', 'instrumentalness', 'key', 'liveness', 'danceability', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'energy', 'release_date',  'year', 'decade', 'letter_keys', 'modes', 'key_mode', 'scaled_speech', 'scaled_danceability', 'scaled_instrumentalness', 'scaled_duration', 'scaled_loudness', 'scaled_tempo', 'scaled_energy', 'scaled_popularity', 'A Minor', 'Ab Major', 'Ab Minor', 'B Major', 'B Minor', 'Bb Major', 'Bb Minor', 'C Major', 'C Minor', 'D Major', 'D Minor', 'Db Major', 'Db Minor', 'E Major', 'E Minor', 'Eb Major', 'Eb Minor', 'F Major', 'F Minor', 'F# Major', 'F# Minor', 'G Major', 'G Minor','1960', '1970', '1980', '1990', '2000', '2010', '2020']
    playlist_df = playlist_df.reindex(columns=desired_columns).fillna(False)
    
    # Sonuçları bir Excel dosyasına yaz
    playlist_df.to_excel('model/data/output_playlist_df.xlsx', index=False)

    return playlist_df