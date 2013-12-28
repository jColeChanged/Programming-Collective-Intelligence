"""
Exercise 2 - Boolean Operations

Expand the search engine query system to support multiple queries.
"""
from searchengine import searchengine

engine = searchengine.Searcher("searchengine/searchindex.db")

def or_merge(results_one, results_two):
    merged_list = []
    results_one = []
    # Look at the start of the list
    while len(results_one) or len(results_two):
        if not len(results_one):
            merged_list.extend(results_two)
            break
        elif not len(results_two):
            merged_list.extend(results_one)
            break
        if results_one[0][0] == results_two[0][0]:
            one = results_one.pop(0)
            two = results_two.pop(0)
            average = (one[0], (one[1] + two[1]) / 2.)
            merged_list.append(average)
        elif results_one[0] < results_two[0]:
            merged_list.append(results_one.pop(0))
        else:
            merged_list.append(results_two.pop(0))
    return merged_list


def or_query(query_one, query_two):
    query_one = query_one.lower()
    query_two = query_two.lower()

    rows_one, word_ids_one = engine.get_match_rows(query_one)
    scores_one = engine.get_scored_list(rows_one, word_ids_one)
    scores_one = [(url, score) for (url, score) in scores_one.items()]

    rows_two, word_ids_two = engine.get_match_rows(query_two)
    scores_two = engine.get_scored_list(rows_two, word_ids_two)
    scores_two = [(url, score) for (url, score) in scores_two.items()]

    merged_scores = or_merge(scores_one, scores_two)

    ranked_scores = sorted([(score, url) for (url, score) in merged_scores], reverse=True)
    for score, url_id in ranked_scores[0:10]:
        print '%f\t%s' % (score, engine.get_url_name(url_id))