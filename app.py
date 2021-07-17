import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
import spotifystats
import dataanalysis

app = Flask(__name__)

#  Client Keys
CLIENT_ID = "8693ea1d690a4327905cc28cabfd8fe5"
CLIENT_SECRET = "34003454bd434ab1b813d1f592768d24"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    spotify = spotifystats.SpotifyStats()
    config = spotify.config()
    tracks = spotify.get_tracks(config, "medium_term")
    all_songs = spotify.list_all_songs()

    x = 0
    top_albums = all_songs["album"]
    top_songs = all_songs["song"]
    top_artists = all_songs["artist"]
    top_popularity = all_songs["popularity"]
   
    track_hold = {'artist': top_albums, 'song': top_songs, 
    'album': top_artists, 'popularity': top_popularity}
    track_hold = zip(track_hold['artist'],track_hold['song'], track_hold['album'], track_hold['popularity'])

    # Combine profile and playlist data to display
    return render_template("index.html", x = track_hold)

if __name__ == "__main__":
    spotify = spotifystats.SpotifyStats()
    config = spotify.config()
    tracks = spotify.get_tracks(config, "medium_term")
    all_songs = spotify.list_all_songs()

    # generate pyplots
    dataanalysis.plot_songs_per_artist(all_songs)

    app.run(debug=True, port=PORT)