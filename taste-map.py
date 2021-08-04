#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
taste-map.py: 
	Visualizing your Spotify music tastes with Matplotlib using Spotipy API.
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
import pandas
import pprint
import time
import pickle
import sys

# Establish authorization arguments
redirect_uri = 'https://example.com/callback'
scope = 'user-library-read'
offset = 0
limit = 50
saved_tracks = []

pp = pprint.PrettyPrinter(depth=6) # Establishing pretty print

# Connect to spotify API (first build has to be in terminal)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Find the number of tracks the user has saved
total_tracks = sp.current_user_saved_tracks(limit=1, offset=offset)['total']
# total_tracks = 10

while len(saved_tracks) < total_tracks:
	try: 
		# Grab a batch of tracks
		fetch_request = sp.current_user_saved_tracks(limit=limit, offset=offset)
		for track in fetch_request['items']:
			saved_tracks.append(track) # Add to list of saved tracks
		
		# Change offset to move batch target
		offset = fetch_request['offset'] + fetch_request['limit']
		print("Pulling saved tracks: %.2f%% complete..." % ((len(saved_tracks) / total_tracks)*100))
		time.sleep(0.5)
	except Exception as e:
		print("Saving tracks failed: ", e)
		print(len(saved_tracks) + " out of " + total_tracks + " saved...")

# pp.pprint(saved_tracks)

# Write saved songs to pickled file
with open("saved_tracks.config", "wb") as f:
	pickle.dump(saved_tracks, f, pickle.HIGHEST_PROTOCOL)

# Read saved songs from pickled file
with open("saved_tracks.config", "rb") as f:
	unpickled_saved = pickle.load(f)

for i in range(len(unpickled_saved)):
	print("%d) %s -- %s" % (i+1, unpickled_saved[i]['track']['name'], unpickled_saved[i]['track']['artists'][0]['name']))

# pp.pprint(unpickled_saved)

# TODO: Visualization functions
	
	# TODO: 

