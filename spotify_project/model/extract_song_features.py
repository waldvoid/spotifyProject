import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from dotenv import load_dotenv
import os




def extract_song_features(song):
    load_dotenv()
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Audio features
    features = sp.audio_features(song)[0]

    # Artist of the track, for genres and energy
    artist = sp.track(song)["artists"][0]["id"]
    artist_name = sp.artist(artist)["name"]
    artist_pop = sp.artist(artist)["energy"]
    artist_genres = sp.artist(artist)["genres"]

    # Track energy
    track_pop = sp.track(song)["energy"]
    track_name = sp.track(song)["name"]
    track_id = sp.track(song)["id"]

    # Add features
    features["track_id"] = track_id
    features["track_name"] = track_name
    features["artist_name"] = artist_name
    features["artist_pop"] = artist_pop
    features["track_pop"] = track_pop
    if artist_genres:
        features["genres"] = " ".join([re.sub(' ', '_', i) for i in artist_genres])
    else:
        features["genres"] = "unknown"
    return features


if __name__ == "__main__":
    # Debug
    result = extract_song_features("37xXDxPzfk5lnU8aNSRXfw")
    print(result)


