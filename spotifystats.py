import os
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

class SpotifyStats():

    def config(self):
        config = {"client_id": "value1", "client_secret": "value2"}

        with open('config.json', 'r') as f:
            config = json.load(f)
        return config

    # time range can be "short_term", "medium_term", "long_term"
    def get_tracks(self, config, range):

        # get client id, uri, secret from config
        REDIRECT_URI ='http://localhost:8080/'
        CLIENT_ID = config["client_id"]
        CLIENT_SECRET=config["client_secret"]
        scope = 'user-top-read'

        # set os environ variables
        os.environ['SPOTIPY_CLIENT_ID']= CLIENT_ID
        os.environ['SPOTIPY_CLIENT_SECRET']= CLIENT_SECRET
        os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8080/'

        # authorization flow –> user should input user/pass upon first login
        username = ""
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
        else:
            print("Can't get token for", username)


if (__name__ == "__main__"):
    spotifyStats = SpotifyStats()
    config = spotifyStats.config()
    tracks = spotifyStats.get_tracks(config, "medium_term")

    print("Loading your top 50 songs...")

