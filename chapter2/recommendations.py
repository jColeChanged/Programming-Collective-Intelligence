from math import sqrt

# A dictionary of movie critics and their ratings of a small set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
	'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
	'The Night Listener': 3.0},
	'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
	'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
	'You, Me and Dupree': 3.5},
	'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
	'Superman Returns': 3.5, 'The Night Listener': 4.0},
	'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
	'The Night Listener': 4.5, 'Superman Returns': 4.0,
	'You, Me and Dupree': 2.5},
	'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
	'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
	'You, Me and Dupree': 2.0},
	'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
	'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
	'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def transform_prefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})

			# Flip item and person
			result[item][person] = prefs[person][item]
	return result

movies = transform_prefs(critics)
def sim_distance(prefs, person1, person2):
	"""
	Return a distance-based similarity score for person1 and person2. The 
	value returned will always between 0 and 1. A value of 1 indicates that 
	the users are similar to each other. A rating of zero indicates the users 
	are different from each other.
	"""
	# Build a list of shared items
	shared_interests = []
	for item in prefs[person1]:
		if item in prefs[person2]:
			shared_interests.append(item)

	if len(shared_interests) == 0:
		return 0

	euclidean_distance = sqrt(sum([pow(prefs[person1][item]-prefs[person2][item], 2)
						           for item in shared_interests]))
	return 1 / (1 + euclidean_distance)

def sim_pearson(prefs, person1, person2):
	"""
	Returns the Person corellation coefficient for p1 and p2.
	"""
	shared_interests = [item for item in prefs[person1] if item in prefs[person2]]

	n = float(len(shared_interests))
	if n == 0:
		return 0

	# Add up the prefrences
	sum1 = sum([prefs[person1][interest] for interest in shared_interests])
	sum2 = sum([prefs[person2][interest] for interest in shared_interests])

	# Sum up the squares
	sum1Sq = sum([pow(prefs[person1][interest], 2) for interest in shared_interests])
	sum2Sq = sum([pow(prefs[person2][interest], 2) for interest in shared_interests])

	# Sum up the products
	pSum = sum([prefs[person1][interest] * prefs[person2][interest] 
			    for interest in shared_interests])

	num = pSum - (sum1 * sum2 / n)
	den = sqrt((sum1Sq -pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

	return num / den if den else 0



def top_matches(prefs, person, n=5, similarity=sim_pearson):
	"""
	prefs: a dictionary of prefrences
	person: the person to compare prefrences with
	n: number of results to return
	similiarty: the function to use to see how similar two users are

	Returns the best matches for person from the prefs dictionary.
	"""
	scores = [(similarity(prefs, person, other), other)
			  for other in prefs if other != person]
	# Sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()
	return scores[0:n]

def get_recommendations(prefs, person, similarity=sim_pearson):
	"""
	Gets recommendations for a person by using a weighted average of every
	other user's ranking.
	"""
	totals = {}
	sim_sums = {}
	for other in prefs:
		if other == person: continue
		sim = similarity(prefs, person, other)

		# ignore scores of zero or lower
		if sim <= 0: continue
		for item in prefs[other]:
			# Only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim

				sim_sums.setdefault(item, 0)
				sim_sums[item] += sim
	# Create the normalized list
	rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

	# Return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings

def calculate_similar_items(prefs, n=10):
	"""
	Returns a dictionary of items showing which other items they
	are most similar to.
	"""
	result = {}
	# Invert the prefrence matrix to be item centric.
	itemPrefs = transform_prefs(prefs)
	c = 0
	for item in itemPrefs:
		# Status updates for large datasets
		c += 1
		if c % 100 == 0:
			print "%d / %d" % (c, len(itemPrefs))
		# Find the most similar items to this one.
		scores = top_matches(itemPrefs, item, n=n, similarity=sim_distance)
		result[item] = scores
	return result

def get_recommended_items(prefs, item_match, user):
	user_ratings = prefs[user]
	scores = {}
	total_sim = {}
	for (item, rating) in user_ratings.items():
		# Ignore items the user has already rated
		for (similarity, item2) in item_match[item]:
			# ignore if seen
			if item2 in user_ratings: continue

			# Weightted sum of rating times sim
			scores.setdefault(item2, 0)
			scores[item2] += similarity * rating

			# Sum of all the similarities
			total_sim.setdefault(item2, 0)
			total_sim[item2] += similarity

	# Get the a weighted average for each
	rankings = [(score/total_sim[item], item)
				    for item, score in scores.items()]
	rankings.sort()
	rankings.reverse()
	return rankings

def load_movie_lens(path='movielens'):
	# Get movie titles
	movies = {}
	for line in open(path + "/u.item"):
		id, title = line.split("|")[:2]
		movies[id] = title

	# load data
	prefs = {}
	for line in open(path+ "/u.data"):
		user, movieid, rating, ts = line.split("\t")
		prefs.setdefault(user, {})
		prefs[user][movies[movieid]] = float(rating)
	return prefs


