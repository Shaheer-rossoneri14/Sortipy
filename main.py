from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import cred


app = Flask(__name__)

@app.route("/home", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route("/about", methods=['POST', 'GET'])
def about():
    return render_template("about.html")


@app.route('/sortipy', methods=['POST', 'GET'])
def sortipy():
    #Get user Playlist
    URL = request.form['URL'] 

    #Authenticate request 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url))

    #Get playlist ID
    playlist_id = URL.split("/")[4].split("?")[0]

    #Get Playlist Tracks and track metadata
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    results = tracks    

    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_popularity = []

    for i in range(len(results)):
        if i == 0:
            playlist_tracks_id = results[i]['track']['id']
            playlist_tracks_titles = results[i]['track']['name']
            playlist_tracks_popularity = results[i]['track']['popularity']

            artist_list = []
            for artist in results[i]['track']['artists']:
                artist_list= artist['name']
            playlist_tracks_artists = artist_list

            #Get Audio features of the tracks
            features = sp.audio_features(playlist_tracks_id)

            #Store all the track metadata and audio features in a dataframe
            features_df = pd.DataFrame(data=features, columns=features[0].keys())
            features_df['title'] = playlist_tracks_titles
            features_df['artists'] = playlist_tracks_artists
            features_df['popularity'] = playlist_tracks_popularity
            features_df = features_df[['title', 'artists', 'popularity',
                                       'danceability', 'energy', 'key', 'loudness',
                                       'mode', 'acousticness', 'instrumentalness',
                                       'liveness', 'valence', 'tempo',
                                       'duration_ms']]
            continue
        else:
            #spotipy limits at 100 tracks.
            #if number of tracks is greater than 100.
            try: 
                playlist_tracks_id = results[i]['track']['id']
                playlist_tracks_titles = results[i]['track']['name']
                playlist_tracks_popularity = results[i]['track']['popularity']
                artist_list = []
                for artist in results[i]['track']['artists']:
                    artist_list= artist['name']
                playlist_tracks_artists = artist_list
                features = sp.audio_features(playlist_tracks_id)
                new_row = {'title':[playlist_tracks_titles],
               'artists':[playlist_tracks_artists],
               'popularity':[playlist_tracks_popularity],
               'danceability':[features[0]['danceability']],
               'energy':[features[0]['energy']],
               'key':[features[0]['key']],
               'loudness':[features[0]['loudness']],
               'mode':[features[0]['mode']],
               'acousticness':[features[0]['acousticness']],
               'instrumentalness':[features[0]['instrumentalness']],
               'liveness':[features[0]['liveness']],
               'valence':[features[0]['valence']],
               'tempo':[features[0]['tempo']],
               'duration_ms':[features[0]['duration_ms']],
               }

                dfs = [features_df, pd.DataFrame(new_row)]
                features_df = pd.concat(dfs, ignore_index = True)
            except:
                continue
    global df1
    df1 = features_df
    return render_template("index.html", column_names=df1.columns.values, row_data=list(df1.values.tolist()),zip=zip)            

    
@app.route('/danceability', methods=['POST', 'GET'])
def danceability():
    dfdance = df1.sort_values(by=['danceability'], ascending=False)
    return render_template("danceability.html", column_names=dfdance.columns.values, row_data=list(dfdance.values.tolist()),zip=zip)


@app.route('/energy', methods=['POST', 'GET'])
def energy():
    dfenergy = df1.sort_values(by=['energy'], ascending=False)
    return render_template("energy.html", column_names=dfenergy.columns.values, row_data=list(dfenergy.values.tolist()),zip=zip)


@app.route('/loudness', methods=['POST', 'GET'])
def loudness():
    dfloudness = df1.sort_values(by=['loudness'], ascending=False)
    return render_template("loudness.html", column_names=dfloudness.columns.values, row_data=list(dfloudness.values.tolist()),zip=zip)


@app.route('/acousticness', methods=['POST', 'GET'])
def acousticness():
    dfacoustic = df1.sort_values(by=['acousticness'], ascending=False)
    return render_template("acousticness.html", column_names=dfacoustic.columns.values, row_data=list(dfacoustic.values.tolist()),zip=zip)


@app.route('/instrumentalness', methods=['POST', 'GET'])
def instrumentalness():
    dfinstrumental = df1.sort_values(by=['instrumentalness'], ascending=False)
    return render_template("instrumentalness.html", column_names=dfinstrumental.columns.values, row_data=list(dfinstrumental.values.tolist()),zip=zip)


@app.route('/liveness', methods=['POST', 'GET'])
def liveness():
    dfliveness = df1.sort_values(by=['liveness'], ascending=False)
    return render_template("liveness.html", column_names=dfliveness.columns.values, row_data=list(dfliveness.values.tolist()),zip=zip)


@app.route('/valence', methods=['POST', 'GET'])
def valence():
    dfvalence = df1.sort_values(by=['valence'], ascending=False)
    return render_template("valence.html", column_names=dfvalence.columns.values, row_data=list(dfvalence.values.tolist()),zip=zip)


@app.route('/tempo', methods=['POST', 'GET'])
def tempo():
    dftempo = df1.sort_values(by=['tempo'], ascending=False)
    return render_template("tempo.html", column_names=dftempo.columns.values, row_data=list(dftempo.values.tolist()),zip=zip)


@app.route('/popularity', methods=['POST', 'GET'])
def popularity():
    dfpopularity = df1.sort_values(by=['popularity'], ascending=False)
    return render_template("popularity.html", column_names=dfpopularity.columns.values, row_data=list(dfpopularity.values.tolist()),zip=zip)   


if __name__ == "__main__":
    app.run(debug=True)
