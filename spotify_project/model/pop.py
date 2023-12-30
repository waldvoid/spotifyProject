import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)


# Spotipy nesnesi oluştur
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Şarkı URI'sini belirle
song_uri = '2OtqcaKH0R8ejfaTdt1iO4'

# Şarkı bilgilerini API'dan çek
track = sp.track(song_uri)

# Popularity (popülerlik) değerini al
popularity = track['popularity']
print(f"Şarkı Popülerliği: {popularity}")


