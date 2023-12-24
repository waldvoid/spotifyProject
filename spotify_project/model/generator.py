import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from model.extract_playlist_features import extract_playlist_features
def generate_recommendations(playlist_url):
    # Önceden işlenmiş büyük veri setini yükle
    labels_df = pd.read_excel('model/data/output.xlsx')
    labels_id = labels_df['id']
    labels_name = labels_df['name']
    labels_artists = labels_df['artists']
    labels_df = labels_df.drop(['release_date', 'name', 'id', 'artists', 'mode', 'letter_keys', 'speechiness', 'year', 'decade', 'modes', 'key_mode', 'instrumentalness', 'key', 'liveness', 'loudness', 'tempo', 'popularity'], axis=1)

    # NaN değerleri 0 ile doldur
    labels_df = labels_df.fillna(0)

    # Kullanıcının çalma listesini al ve özelliklerini çıkar
    playlist_df = extract_playlist_features(playlist_url)

    # gereksiz sütunları çalma listesinden çıkar
    playlist_id = playlist_df['id']
    playlist_name = playlist_df['name']
    playlist_artists = playlist_df['artists']
    playlist_df = playlist_df.drop(['release_date', 'id', 'name', 'artists', 'mode',  'speechiness', 'letter_keys', 'year',  'decade', 'modes', 'key_mode', 'instrumentalness', 'key', 'liveness', 'loudness', 'tempo', 'popularity'], axis=1)

    # Float özelliklere ağırlık atama
    float_features = {
        'valence': 1.2,
        'scaled_speech': 1.1,
        'scaled_duration': 1,
        'scaled_loudness': 1.3,
        'scaled_tempo': 1.4,
        'scaled_pop': 1.1,
        'scaled_instrumentalness': 1.2,
    }

    for feature, weight in float_features.items():
        playlist_df[feature] = playlist_df[feature] * weight
        labels_df[feature] = labels_df[feature] * weight

    # Boolean özelliklere ağırlık atama
    boolYear_features = ['1960', '1970', '1980', '1990', '2000', '2010', '2020']
    for feature in boolYear_features:
        playlist_df[feature] = playlist_df[feature].apply(lambda x: 1.3 if x else 0)
        labels_df[feature] = labels_df[feature].apply(lambda x: 1.3 if x else 0)

    # Boolean özelliklere ağırlık atama
    boolMode_features = ['A Minor', 'Ab Major', 'Ab Minor', 'B Major', 'B Minor', 'Bb Major', 'Bb Minor', 'C Major', 'C Minor', 'D Major', 'D Minor', 'Db Major', 'Db Minor', 'E Major', 'E Minor', 'Eb Major', 'Eb Minor', 'F Major', 'F Minor', 'F# Major', 'F# Minor', 'G Major', 'G Minor']
    for feature in boolMode_features:
        playlist_df[feature] = playlist_df[feature].apply(lambda x: 1 if x else 0)
        labels_df[feature] = labels_df[feature].apply(lambda x: 1 if x else 0)

    # Veri setini ölçeklendir
    scaler = StandardScaler()
    labels_df_scaled = scaler.fit_transform(labels_df)

    # NaN değerleri 0 la doldur
    playlist_df = playlist_df.fillna(0)

    # Kullanıcının çalma listesini ölçeklendir
    playlist_df_scaled = scaler.transform(playlist_df)

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

    # Kullanıcının çalma listesindeki her şarkı için bir küme etiketi tahmin et
    playlist_df['cluster'] = kmeans.predict(playlist_df_scaled)
    labels_df['cluster'] = kmeans.predict(labels_df_scaled)

    labels_df['id'] = labels_id
    labels_df['name'] = labels_name
    labels_df['artists'] = labels_artists

    playlist_df['id'] = playlist_id
    playlist_df['name'] = playlist_name
    playlist_df['artists'] = playlist_artists

    print(playlist_df)

    # Her bir küme için, kullanıcının çalma listesindeki şarkılara en benzer olan şarkıları bul
    recommendations = pd.DataFrame()
    for cluster in playlist_df['cluster'].unique():
        # Bu kümeye ait şarkıları al
        cluster_songs = labels_df[labels_df['cluster'] == cluster]

        # Kullanıcının çalma listesindeki bu kümeye ait şarkıları al
        user_songs = playlist_df[playlist_df['cluster'] == cluster]

        # Kullanıcının şarkıları ile kümeye ait tüm şarkılar arasında kosinüs benzerliğini hesapla
        similarity_matrix = cosine_similarity(user_songs.drop(['cluster', 'name', 'id', 'artists'], axis=1), cluster_songs.drop(['cluster', 'name', 'id', 'artists'], axis=1))

        # Her bir kullanıcı şarkısı için, en benzer olan 5 şarkıyı al
        for i in range(similarity_matrix.shape[0]):
            top_5_similar_songs = cluster_songs.iloc[similarity_matrix[i].argsort()[-5:][::-1]]
            recommendations = pd.concat([recommendations, top_5_similar_songs])

    # Remove duplicate songs based on 'id' column
    recommendations = recommendations.drop_duplicates(subset='id')

    # Önerilen şarkıları bir Excel dosyasına yaz
    recommendations.to_excel('model/data/recommendation.xlsx', index=False)
    playlist_df.to_excel('model/data/playlist_comparison.xlsx', index=False)

    return recommendations[['name', 'artists']]

