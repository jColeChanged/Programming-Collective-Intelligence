"""
Exercise 1

Below I've implemented a tanimato scoring algorithm. The tanimato scoring
algorithm compares two sets to see how similar they are. In cases where
similairty is decided not by how close something is in space but how many
features are shared, it makes sense to use this. For example, the number
of followers someone has on twitter might map well onto this algorithm when
trying to find similar twitter users. So in general its useful when dealing
with binary features.
"""

def sim_tanimato(prefs, person1, person2):
	"""
	Returns the tanimato score for p1 and p2.
	"""
	p1 = set(item for item in prefs[person1] if prefs[person1][item])
	p2 = set(item for item in prefs[person2] if prefs[person2][item])
	union_length = float(len(p1.union(p2)))
	return len(p1.intersection(p2)) / union_length if union_length else 0