"""
Exercise 2

In this exercise I tried to find tags which were similar to each other. The
distance metric that I used was the tanimato score. I felt this was a good
distance metric since it mapped to the proportion of shared tags for each
bookmark and because whether or not a bookmark shared a tag was ultimately
a binary feature. It would either share the tag or not.

"""
from pydelicious import get_tagposts, get_popular
import recommendations
import ex1
import pprint

def build_tag_list(tag, n=20):
	"""
	Given a tag, fetches more tags by crawling for tags. Returns the tags.
	"""
	unprocessed_tags = [tag]
	processed_tags = []

	while len(unprocessed_tags) > 0 and len(unprocessed_tags) + len(processed_tags) < n:
		next_tag = unprocessed_tags.pop()
		bookmarks = get_tagposts(next_tag)
		processed_tags.append(next_tag)
		for bookmark in bookmarks:
			for tag in bookmark["tags"]:
				if tag not in processed_tags and tag not in unprocessed_tags:
					unprocessed_tags.append(tag)

	return (unprocessed_tags + processed_tags)[-n:]

def build_tag_dict(tags):
	all_items = {}
	tags_dict = {}
	# Find links posted by all get_user
	for tag in tags:
		bookmarks = get_popular(tag=tag)
		for bookmark in bookmarks:
			url = bookmark["url"]
			for tag in bookmark["tags"]:
				tags_dict.setdefault(tag, {})
				tags_dict[tag][url] = 1.0
				all_items[url] = 1


	# Fill in missing items with zero.
	for ratings in tags_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item] = 0.0
	return tags_dict

def __main__():
	tags_dict = build_tag_dict(build_tag_list("programming"))
	print "Similar Tags"
	recs = recommendations.top_matches(tags_dict, "programming", similarity=ex1.sim_tanimato)
	pprint.pprint(recs)
	best_rec = recs[0][1]
	print "Similar Tag, But Not Sharing Tags"
	pprint.pprint([tag for tag in tags_dict[best_rec] if tags_dict[best_rec][tag] and not tags_dict["programming"][tag]])

# >>> __main__()
# Similar Tags
# [(0.17391304347826086, u'development'),
#  (0.15789473684210525, u'course'),
#  (0.14285714285714285, u'java'),
#  (0.1, u'coursera'),
#  (0.09090909090909091, u'gwt')]
# Similar Tag, But Not Sharing Tags
# [u'http://wheel.readthedocs.org/en/latest/',
#  u'http://littlegists.blogspot.co.uk/2012/12/building-simple-nancy-app-from-scratch.html',
#  u'http://msdn.microsoft.com/en-us/library/dn155905.aspx',
#  u'http://www.amityadav.name/code-analyzers-for-php/',
#  u'http://www.babycenter.com/0_20-fun-silly-development-boosting-games-to-play-with-your-ba_1479310.bc?scid=momsbaby_20130618:4&pe=MlVEME9CaXwyMDEzMDYxOA..',
#  u'http://edition.cnn.com/2013/06/19/opinion/technology-change-lives-african-women-jamme/?hpt=hp_t5',
#  u'https://django-cookie-consent.readthedocs.org/en/latest/',
#  u'http://www.bbc.co.uk/news/world-22964022',
#  u'https://docs.google.com/presentation/d/1IRHyU7_crIiCjl0Gvue0WY3eY_eYvFQvSfwQouW9368/present#slide=id.gebc26cd7_8_0']