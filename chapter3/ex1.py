"""
Exercise 1

Using the del.icio.us API from Chapter 2, create a dataset of bookmarks 
suitable for clustering. Run hiearchical clustering and k-means clustering 
on it.
"""
from pydelicious import get_tagposts, get_popular
from clusters import draw_dendogram, hcluster

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

def build_tag_matrix(tags):
    """
    Given a list of bookmarks returns a matrix with
    tags as columns and urls as rows.

    Returns: tags, urls, matrix
    """
    bookmarks = []
    for tag in tags:
        marks = get_popular(tag=tag)
        for bookmark in marks:
            url = bookmark["url"]
            tags = bookmark["tags"]
            bookmarks.append({"url": url, "tags": tags})

    tag_list = set(tag for tag in bookmark["tags"] for bookmark in bookmarks)
    url_list = []
    matrix = []
    for bookmark in bookmarks:
        row = []
        for tag in tag_list:
            row.append(1 if tag in bookmark["tags"] else 0)
        url_list.append(bookmark["url"])
        matrix.append(row)
    return tag_list, url_list, matrix

def __main__():
    tag_list = build_tag_list("programming")
    tags, urls, data = build_tag_matrix(tag_list)
    cluster = hcluster(data)
    draw_dendogram(cluster, urls, jpeg="delicious.jpg")



