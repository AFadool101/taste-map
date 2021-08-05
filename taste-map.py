#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
taste-map.py: 
	Visualizing your Spotify music tastes with Matplotlib 
using Spotipy API.
"""

__author__ = "Aidan Fadool"
__copyright__ = "Copyright 2021, Shaky Dev Projects"
__credits__ = ["Aidan Fadool"]

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Aidan Fadool"
__email__ = "fadooljo@msu.edu"
__status__ = "Production"

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import client_id, client_secret
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import pprint
import time
import pickle
import sys

# Establish authorization arguments
redirect_uri = 'https://example.com/callback'
scope = 'user-top-read'
file = "saved_tracks.config"

pp = pprint.PrettyPrinter(depth=4) # Establishing pretty print
pd.set_option("display.max_rows", None, "display.max_columns", None)

def connectToSpotify(c_id, c_secret, redirect_uri, scope):
	# Connect to spotify API (first build has to be in terminal)
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
											   client_secret=c_secret,
											   redirect_uri=redirect_uri,
											   scope=scope))
	return sp

def pickleFile(file, data):
	# Write saved songs to pickled file
	with open(file, "wb") as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def readFromPickle(pickled_file):
	# Read saved songs from pickled file
	with open(pickled_file, "rb") as f:
		return pickle.load(f)

def fetchTrackDetails(track_id):
	# Request details about the track
	track_info = sp.track(track_id)
	track_features = sp.audio_features(track_id)

	# Track Info
	name = track_info['name']
	album = track_info['album']['name']
	artist = track_info['artists'][0]['name']
	release_date = track_info['album']['release_date']
	length = track_info['duration_ms']
	popularity = track_info['popularity']

	# Track Features
	acousticness = track_features[0]['acousticness']
	danceability = track_features[0]['danceability']
	energy = track_features[0]['energy']
	instrumentalness = track_features[0]['instrumentalness']
	liveness = track_features[0]['liveness']
	loudness = track_features[0]['loudness']
	speechiness = track_features[0]['speechiness']
	tempo = track_features[0]['tempo']
	time_signature = track_features[0]['time_signature']
	valence = track_features[0]['valence']

	# Organize data into a list
	track_data = [name, album, artist, release_date, length, popularity, acousticness, danceability, energy, 
				instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]

	return track_data

def fetchArtistDetails(artist_id):
	# Request details about the artist
	artist_info = sp.artist(artist_id)

	# Artist info
	name = artist_info['name']
	followers = artist_info['followers']['total']
	genres = artist_info['genres']
	popularity = artist_info['popularity']
	a_type = artist_info['type']

	# Organize data into a list
	artist_data = [name, followers, genres, popularity, a_type]
	return artist_data


def fetchTopTrackIds(limit, period):
	# Get the user's top listened tracks
	results = sp.current_user_top_tracks(limit=limit, offset=0, time_range=period)
	top_track_ids = [x['id'] for x in results['items']]
	return top_track_ids

def fetchTopArtistIds(limit, period):
	# Get the user's top listened artists
	results = sp.current_user_top_artists(limit=limit, offset=0, time_range=period)
	top_artist_ids = [x['id'] for x in results['items']]
	return top_artist_ids

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()

# Connect to API
sp = connectToSpotify(client_id, client_secret, redirect_uri, scope)

# Get the user's 'most listened'
top_track_ids = fetchTopTrackIds(50, 'medium_term')
top_artist_ids = fetchTopArtistIds(50, 'medium_term')

# Create a list to store dataframe data
track_data_list = []
l = len(top_track_ids)
# Iterate through top tracks
for i in range(len(top_track_ids)):
	track_data = fetchTrackDetails(top_track_ids[i])
	track_data_list.append(track_data)
	time.sleep(0.1)
	# Update Progress Bar
	printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

# Create a list to store dataframe data
artist_data_list = []
l = len(top_artist_ids)
# Iterate through top artists
for i in range(len(top_artist_ids)):
	artist_data = fetchArtistDetails(top_artist_ids[i])
	artist_data_list.append(artist_data)
	time.sleep(0.1)
	# Update Progress Bar
	printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

genre_dict = {} # Dict to hold count of artist genres
# Parse through each artists' genres
for artist in artist_data_list:
	for genre in artist[2]:
		# Check if the genre exists in the dict
		if genre in list(genre_dict.keys()):
			genre_dict[genre] += 1;
		else:
			genre_dict[genre] = 1;

# Turn dict into a nested list
genre_keys = list(genre_dict.keys())
genre_values = list(genre_dict.values())
genre_list = []
for i in range(len(genre_keys)):
	genre_pair = [genre_keys[i], genre_values[i]]
	genre_list.append(genre_pair)

# Create the tracks dataframe
top_tracks_df = pd.DataFrame(track_data_list, columns=['Name', 'Album', 'Artist', 'Realease Date', 'Length (ms)', 'Popularity', 
											'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 
											'Loudness', 'Speechiness', 'Tempo', 'Time Signature', 'Valence'])

# Create the artists dataframe
top_artists_df = pd.DataFrame(artist_data_list, columns=['Name', 'Followers', 'Genres', 'Popularity', 'Type'])

# Create the genre dataframe
genres_df = pd.DataFrame(genre_list, columns=['Genre', 'Count'])
genres_df_filtered = genres_df[genres_df['Count'] > 2]

# Tracks Breakdown Scatter Plot
tracks_scatter_fig = px.scatter(top_tracks_df, x=top_tracks_df['Tempo'], y=top_tracks_df['Danceability'], color=top_tracks_df['Popularity'], 
					size=top_tracks_df['Popularity'], title='Plot of Song Popularity using Tempo against Danceability',
					hover_name=top_tracks_df['Name'])

# Genre breakdown Pie Chart
genre_pie_fig = px.pie(genres_df_filtered, names='Genre', values='Count', title='Your Genre Breakdown')

tracks_scatter_fig.show()
genre_pie_fig.show()
