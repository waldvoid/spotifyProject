import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

SPOTIPY_CLIENT_ID = 'ff34a979c12f4b9db36eeb34edcef3ce'
SPOTIPY_CLIENT_SECRET = 'f5df5d6fbfe34a6fb59ac82e28e9dc41'



def extract_song_features(song):
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Audio features
    features = sp.audio_features(song)[0]

    # Artist of the track, for genres and popularity
    artist = sp.track(song)["artists"][0]["id"]
    artist_name = sp.artist(artist)["name"]
    artist_pop = sp.artist(artist)["popularity"]
    artist_genres = sp.artist(artist)["genres"]

    # Track popularity
    track_pop = sp.track(song)["popularity"]
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


