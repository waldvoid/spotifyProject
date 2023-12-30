import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from model.extract_playlist_features import extract_playlist_features

def generate_recommendations(playlist_url, sp):

    # Önceden işlenmiş büyük veri setini yükle
    labels_df = pd.read_csv('model/data/output.csv')
    labels_id = labels_df['id']
    labels_uri = labels_df['uri']
    labels_df = labels_df.drop(['release_date', 'uri', 'id', 'mode', 'danceability', 'letter_keys', 'speechiness', 'year', 'decade', 'modes', 'key_mode', 'instrumentalness', 'key', 'liveness', 'loudness', 'tempo', 'energy', 'popularity'], axis=1)

    # NaN değerleri 0 ile doldur
    labels_df = labels_df.fillna(0)

    # Kullanıcının çalma listesini al ve özelliklerini çıkar
    playlist_df = extract_playlist_features(playlist_url, sp)

    # gereksiz sütunları çalma listesinden çıkar
    playlist_id = playlist_df['id']
    playlist_uri = playlist_df['uri']
    playlist_df = playlist_df.drop(['release_date', 'uri', 'id', 'mode', 'danceability',  'speechiness', 'letter_keys', 'year',  'decade', 'modes', 'key_mode', 'instrumentalness', 'key', 'liveness', 'loudness', 'tempo', 'energy', 'popularity'], axis=1)

    # Float özelliklere ağırlık atama
    float_features = {
        'valence': 1,
        'scaled_speech': 1,
        'scaled_duration': .8,
        'scaled_loudness': 1,
        'scaled_tempo': 1,
        'scaled_energy': 1,
        'scaled_instrumentalness': 1,
        'scaled_danceability': 1,
        'scaled_popularity': 1.1,
    }

    for feature, weight in float_features.items():
        playlist_df[feature] = playlist_df[feature] * weight
        labels_df[feature] = labels_df[feature] * weight

    # Boolean özelliklere ağırlık atama
    boolYear_features = ['1960', '1970', '1980', '1990', '2000', '2010', '2020']
    for feature in boolYear_features:
        playlist_df[feature] = playlist_df[feature].apply(lambda x: 1.1 if x else 0)
        labels_df[feature] = labels_df[feature].apply(lambda x: 1.1 if x else 0)

    # Boolean özelliklere ağırlık atama
    boolMode_features = ['A Minor', 'Ab Major', 'Ab Minor', 'B Major', 'B Minor', 'Bb Major', 'Bb Minor', 'C Major', 'C Minor', 'D Major', 'D Minor', 'Db Major', 'Db Minor', 'E Major', 'E Minor', 'Eb Major', 'Eb Minor', 'F Major', 'F Minor', 'F# Major', 'F# Minor', 'G Major', 'G Minor']
    for feature in boolMode_features:
        playlist_df[feature] = playlist_df[feature].apply(lambda x: 1.1 if x else 0)
        labels_df[feature] = labels_df[feature].apply(lambda x: 1.1 if x else 0)

    # Veri setini ölçeklendir
    scaler = StandardScaler()
    labels_df_scaled = scaler.fit_transform(labels_df)

    # NaN değerleri 0 la doldur
    playlist_df = playlist_df.fillna(0)

    # Kullanıcının çalma listesini ölçeklendir
    playlist_df_scaled = scaler.transform(playlist_df)

    print('data scaled')

    # Optimal küme sayısını belirle
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(labels_df_scaled)
        wcss.append(kmeans.inertia_)

    # Elbow noktasını bul
    n_clusters = wcss.index(min(wcss)) + 1

    # KMeans modelini eğit
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(labels_df_scaled)

    print('kmeans trained')

    # Kullanıcının çalma listesindeki her şarkı için bir küme etiketi tahmin et
    playlist_df['cluster'] = kmeans.predict(playlist_df_scaled)
    labels_df['cluster'] = kmeans.predict(labels_df_scaled)

    labels_df['id'] = labels_id
    labels_df['uri'] = labels_uri

    playlist_df['id'] = playlist_id
    playlist_df['uri'] = playlist_uri

   

    # Her bir küme için, kullanıcının çalma listesindeki şarkılara en benzer olan şarkıları bul
    recommendations = pd.DataFrame()
    for cluster in playlist_df['cluster'].unique():
        # Bu kümeye ait şarkıları al
        cluster_songs = labels_df[labels_df['cluster'] == cluster]

        # Kullanıcının çalma listesindeki bu kümeye ait şarkıları al
        user_songs = playlist_df[playlist_df['cluster'] == cluster]

        # Kullanıcının şarkıları ile kümeye ait tüm şarkılar arasında kosinüs benzerliğini hesapla
        similarity_matrix = cosine_similarity(user_songs.drop(['cluster', 'uri', 'id',], axis=1), cluster_songs.drop(['cluster', 'uri', 'id'], axis=1))

        # Her bir kullanıcı şarkısı için, en benzer olan 5 şarkıyı al
        for i in range(similarity_matrix.shape[0]):
            top_4_similar_songs = cluster_songs.iloc[similarity_matrix[i].argsort()[-4:][::-1]]
            recommendations = pd.concat([recommendations, top_4_similar_songs])

    print('recommendations generated')

    recommendations['new_uri'] = recommendations['uri'].apply(lambda x: 'https://open.spotify.com/intl-tr/track/' + x.replace('spotify:track:', ''))

    print('uri generated')  


    # Önerilen şarkıları bir Excel dosyasına yaz
    recommendations.to_excel('model/data/recommendation.xlsx', index=False)
    playlist_df.to_excel('model/data/playlist_comparison.xlsx', index=False)
    print('excel written')
    
    print('done')
    return recommendations[['new_uri', 'uri']]