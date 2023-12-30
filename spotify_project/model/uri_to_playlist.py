import requests
from model.generator import generate_recommendations
import spotipy
from dotenv import load_dotenv
import os
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import time

def get_full_songs(playlist_url):
    load_dotenv()
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

    # Token al
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = sp.auth_manager.get_access_token(as_dict=False)  # Token'ı al

    song_urls = generate_recommendations(playlist_url, sp)

    new_uris = song_urls['new_uri']
    song_names = []
    song_artists = []
    song_uris = song_urls['uri']

    for uri in song_uris:
        track_id = uri.split(':')[-1]
        response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}",
                                headers={"Authorization": f"Bearer {token}"})  # Token'ı kullan
        if response.status_code == 429:
            # Too many requests, sleep for a bit
            print("Too many requests, sleeping...")
            time.sleep(60)  # 5 seconds
            continue
        elif response.status_code != 200:
            print(f"Error with status code {response.status_code}: {response.text}")
            continue
        track = response.json()
        song_names.append(track['name'])
        song_artists.append(track['artists'][0]['name'])

    return pd.DataFrame({
        'Song': song_names,
        'Artist': song_artists,
        'Listen': new_uris,
    })