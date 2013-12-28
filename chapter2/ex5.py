"""
Exercise 5
"""
import pylast
from ex5secrets import API_KEY, API_SECRET, username, password_hash

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)

seed_track = network.get_track("Daft Punk", "Get Lucky")

def build_user_list(track):
	return [top.item for top in seed_track.get_top_fans()]

def construct_prefs_dict(user_list):
	prefs = {}
	all_tracks = set()
	for user in user_list:
		prefs[user] = {}
		loved_tracks = [loved.track for loved in user.get_loved_tracks()]
		for track in loved_tracks:
			prefs[user][track] = 1.0
			all_tracks.add(track)

	for track in all_tracks:
		for ratings in prefs.values():
			if track not in ratings:
				ratings[track] = 0.0
	return prefs

user_ratings = construct_prefs_dict(build_user_list(seed_track))