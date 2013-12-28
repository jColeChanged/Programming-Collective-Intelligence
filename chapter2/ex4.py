"""
Exercise 4
"""
import deliciousrec
import recommendations

#users = deliciousrec.initialize_user_dict('programming')
#deliciousrec.fill_items(users)

#similar_bookmarks = recommendations.calculate_similar_items(users)

def recommend_bookmarks(prefs, similar_table, user):
	return recommendations.get_recommended_items(prefs, similar_bookmarks, user)

# I'm getting an empty list from my function, but I don't know what I'm doing wrong.