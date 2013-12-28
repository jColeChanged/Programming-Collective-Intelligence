from pydelicious import get_popular, get_userposts, get_urlposts, get_tagposts
import recommendations
import time
import pprint


def initialize_user_dict(tag, count=5):
	user_dict = {}
	for p1 in get_popular(tag=tag)[0:count]:
		for p2 in get_urlposts(p1['url']):
			user = p2['user']
			if user:
				user_dict[user] = {}
	return user_dict

def fill_items(user_dict):
	all_items = {}
	# Find links posted by all get_user
	for user in user_dict:
		for i in range(3):
			posts = []
			try:
				posts = get_userposts(user)
				break
			except:
				print "Failed user " + user + ", retrying."
				time.sleep(4)
		for post in posts:
			url = post["url"]
			user_dict[user][url] = 1.0
			all_items[url] = 1

	# Fill in missing items with zero.
	for ratings in user_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item] = 0.0


#USER_DICT = initialize_user_dict('programming')
#fill_items(USER_DICT)

def run_examples():
	import random
	user = USER_DICT.keys()[random.randint(0, len(USER_DICT) - 1)]
	print user
	top = recommendations.top_matches(USER_DICT, user)
	print top
	recs = recommendations.get_recommendations(USER_DICT, user)[:10]
	print recs
	url = recs[0][1]
	more_top = recommendations.top_matches(recommendations.transform_prefs(USER_DICT), url)
	print more_top





