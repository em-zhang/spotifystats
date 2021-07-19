import os
import json
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from flask import Flask

app = Flask(__name__)

# configure grabs key client information from config.json file
def configure():
    config = {"client_id": "value1", "client_secret": "value2"}
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
    
def get_tracks(config, range):
    # get client id, uri, secret from config
    config = configure()
    username= config["username"]
    CLIENT_ID = config["client_id"]
    CLIENT_SECRET=config["client_secret"]
    CLIENT_SIDE_URL = "http://127.0.0.1"
    PORT = 5000
    REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
    scope = 'user-top-read'

    # set os environ variables
    os.environ['SPOTIPY_CLIENT_ID']= CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET']= CLIENT_SECRET
    os.environ['SPOTIPY_REDIRECT_URI']=REDIRECT_URI

    # authorization flow, user will input user/pass upon first login
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        # get results and write to json file
        results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
        list = []
        list.append(results)
        with open('top50_data.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
        print("Getting token for", username)
    else:
        print("Can't get token for", username)

# returns a list of all songs and generates csv to save data
def list_all_songs():
     with open('top50_data.json') as f:
        data = json.load(f)

    # grab results by category from json
        list_of_results = data[0]["items"]
        list_of_artist_names = []
        list_of_artist_uri = []
        list_of_song_names = []
        list_of_song_uri = []
        list_of_durations_ms = []
        list_of_explicit = []
        list_of_albums = []
        list_of_popularity = []

        for result in list_of_results:
            result["album"]
            this_artists_name = result["artists"][0]["name"]
            list_of_artist_names.append(this_artists_name)
            this_artists_uri = result["artists"][0]["uri"]
            list_of_artist_uri.append(this_artists_uri)
            list_of_songs = result["name"]
            list_of_song_names.append(list_of_songs)
            song_uri = result["uri"]
            list_of_song_uri.append(song_uri)
            list_of_duration = result["duration_ms"]
            list_of_durations_ms.append(list_of_duration)
            song_explicit = result["explicit"]
            list_of_explicit.append(song_explicit)
            this_album = result["album"]["name"]
            list_of_albums.append(this_album)
            song_popularity = result["popularity"]
            list_of_popularity.append(song_popularity)

        # Create dataframe
        all_songs = pd.DataFrame(
            {'artist': list_of_artist_names,
            'artist_uri': list_of_artist_uri,
            'song': list_of_song_names,
            'song_uri': list_of_song_uri,
            'duration_ms': list_of_durations_ms,
            'explicit': list_of_explicit,
            'album': list_of_albums,
            'popularity': list_of_popularity
            
            })

        songs_csv = all_songs.to_csv('top50_songs.csv')
        return all_songs

if (__name__ == "__main__"):
    config = configure()
    tracks = get_tracks(config, "medium_term")

    print("Loading your top 50 songs...")

