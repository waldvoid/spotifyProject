import pandas as pd


# Veri setlerini yükle
data1 = pd.read_excel('model/data/data.xlsx')
data2 = pd.read_excel('model/data/data2.xlsx')

# Veri setlerini birleştir
data = pd.concat([data1, data2])

# Sütunları yeniden düzenle
desired_columns = ['acousticness', 'artists_names', 'danceability', 'duration_ms', 'energy', 'explicit', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'track_name', 'popularity', 'album_release_date', 'speechiness', 'tempo', 'valence', 'year']
data = data[desired_columns]

# Column isimlerini değiştir
data = data.rename(columns={'track_name': 'name', 'artists_names': 'artists', 'album_release_date': 'release_date'})



# key ve mode sütunlarını seslere çevir
keys = {0:'C', 1:'Db',2:'D',3:'Eb',4:'E',5:'F',6:'F#',7:'G',8:'Ab',9:'A',10:'Bb',11:'B'}
modes = {0:'Minor',1:'Major'}

# yeni sütunları ekle
data['letter_keys'] = data['key'].map(keys)
data['modes'] = data['mode'].map(modes)

# key ve mode sütunlarını birleştir yeni bir sütun oluştur
data['key_mode'] = data['letter_keys'] + " " + data['modes']
data['decade'] = data['year'].apply(lambda x: str(x)[:3]+'0')

# eşik değer ortalamasından 5 aşağı - yukarı standart sapması uygula
for feat in data.columns:
    try:
        abv_5_std = data[feat].mean()+ 5* data[feat].std()
        below_5_std = data[feat].mean()- 5* data[feat].std()
        conditions = [data[feat]>abv_5_std, data[feat]<below_5_std]
        choices = [abv_5_std, below_5_std]
        data[feat] = np.select(conditions, choices, data[feat])
    except:
        pass

# 0-1 arasında standartlaştır
data['scaled_speech'] = (data['speechiness'] - min(data['speechiness'])) / (max(data['speechiness']) - min(data['speechiness']))
data['scaled_duration'] = (data['duration_ms'] - min(data['duration_ms'])) / (max(data['duration_ms']) - min(data['duration_ms']))
data['scaled_instrumentalness'] = (data['instrumentalness'] - min(data['instrumentalness'])) / (max(data['instrumentalness']) - min(data['instrumentalness']))
data['scaled_loudness'] = (data['loudness'] - min(data['loudness'])) / (max(data['loudness']) - min(data['loudness']))
data['scaled_tempo'] = (data['tempo'] - min(data['tempo'])) / (max(data['tempo']) - min(data['tempo']))
data['scaled_pop'] = (data['popularity'] - min(data['popularity'])) / (max(data['popularity']) - min(data['popularity']))

key_dummies = pd.get_dummies(data['key_mode'], drop_first=True)
decade_dummies = pd.get_dummies(data['decade'], drop_first=False)
data = pd.concat([data, key_dummies, decade_dummies], axis=1)
# 1980's'den 2020's'e kadar olan decadeleri ekle
decades = ['1960','1970','1980', '1990', '2000', '2010', '2020']
for decade in decades:
    if decade not in data.columns:
        data[decade] = False


# Sonuçları kaydet
data.info()
data.describe()
desired_columns = ['id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'name', 'artists', 'popularity', 'release_date',  'year', 'decade', 'letter_keys', 'modes', 'key_mode', 'scaled_speech', 'scaled_instrumentalness', 'scaled_duration', 'scaled_loudness', 'scaled_tempo', 'scaled_pop', 'A Minor', 'Ab Major', 'Ab Minor', 'B Major', 'B Minor', 'Bb Major', 'Bb Minor', 'C Major', 'C Minor', 'D Major', 'D Minor', 'Db Major', 'Db Minor', 'E Major', 'E Minor', 'Eb Major', 'Eb Minor', 'F Major', 'F Minor', 'F# Major', 'F# Minor', 'G Major', 'G Minor','1960', '1970', '1980', '1990', '2000', '2010', '2020']
data = data[desired_columns]
data.to_excel('model/data/output.xlsx', index=False)

