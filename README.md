# spotifystats

Collects and visualize data for a user's top 50 Spotify songs and artists.

## Using the App
### Creating an App and Using Your Credentials
Visit the Spotify for Developers dashboard to register your app and get your credentials.
1. Go to https://developer.spotify.com/dashboard/, log in and create a new app.
2. In your Spotify app settings, add http://127.0.0.1:5000/ as a Redirect URI.
3. Once you have created your app, get the Client ID and Client Secret, navigate to the `config.json` file in the directory and replace the `client_id`, `client_secret`, and `username` with your credentials.

### Generating data analysis for your top songs
Running `dataanalysis.py` will generate data visualizations and graphs that analyze data from your top 50 tracks and artists. You should also see a `.csv` file that contains your top 50 songs, artists, and albums.

### Running the app
Use the following commands:
```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

If you don't have flask installed or are looking for an alternative, run `python app.py`.

Navigate to http://127.0.0.1:5000/ to view your top songs and artists.

## Built with
- Spotify Web API
- Python
- Flask
- Pandas
- Matplotlib and Seaborn
- React
- Bootstrap
- HTML/CSS

### Example response for user data
<img width="300" alt="Screen Shot 2021-07-29 at 7 16 55 PM" src="https://user-images.githubusercontent.com/78116228/127589962-b963cc65-87ce-49d2-8677-9cbe75fc7e12.png">
