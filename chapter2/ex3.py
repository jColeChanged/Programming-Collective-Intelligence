"""
Excercise 3
"""
import recommendations

similar_critics = recommendations.calculate_similar_items(recommendations.movies)

def get_precomputed_recommendedations(prefs, similar, user):
	similar_prefs = {}
	for other in similar:
		similar_prefs[other] = prefs[other]
	similar_prefs[user] = prefs[user]
	return recommendations.get_recommendations(similar_prefs, user)

# The precompute recommendations tend to match up extremely well with the more 
# laboriously computed recommendations. Probably because they are generated the
# same way. Larger datasets would probably make this match less exact, but 
# would give huge speed improvements, since all algorithms tend to be fast for 
# small n.

