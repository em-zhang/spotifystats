from flask import Flask, redirect, render_template
from urllib.parse import quote
import spotifystats
import dataanalysis

app = Flask(__name__)

# client configuration and keys
config = spotifystats.configure()
CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]

# spotify url and authorization
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# specify server-side parameters, port, and scope
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = 'user-top-read'

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

# auth step and redirect
@app.route("/")
def index():
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

# callback
@app.route("/callback/q")
def callback():
    # get configuration and collect data 
    config = spotifystats.configure()
    tracks = spotifystats.get_tracks(config, "medium_term")
    all_songs = spotifystats.list_all_songs()

    # grab and organize top 50 data
    x = 0
    top_albums = all_songs["album"]
    top_songs = all_songs["song"]
    top_artists = all_songs["artist"]
    top_popularity = all_songs["popularity"]
   
    track_hold = {'artist': top_albums, 'song': top_songs, 
    'album': top_artists, 'popularity': top_popularity}
    track_hold = zip(track_hold['artist'],track_hold['song'], track_hold['album'], track_hold['popularity'])

    # combine profile and playlist data to display on local site
    return render_template("index.html", x = track_hold)

if __name__ == "__main__":
    config = spotifystats.configure()
    tracks = spotifystats.get_tracks(config, "medium_term")

    print("Loading your top 50 songs...")
    all_songs = spotifystats.list_all_songs()

    # generate pyplots
    dataanalysis.plot_songs_per_artist(all_songs)

    app.run(debug=True, port=PORT)