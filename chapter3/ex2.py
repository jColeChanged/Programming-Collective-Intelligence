"""
Exercise 2

Modify the blog parsing code to cluster individual entries instead of entire 
blogs. Do entries from the same blog cluster together? What about entries from 
the same date.
"""
import feedparser
import re

def get_words(html):
    """
    Removes all html tags and returns a list of words that are normalized
    to lower case.
    """
    # remove html tags
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word != '']

def get_word_counts(entry):
    wc = {}
    if 'summary' in entry:
        summary = entry.summary
    else:
        summary = entry.description
    words = get_words(entry.title + ' ' + summary)
    for word in words:
        wc.setdefault(word, 0)
        wc[word] += 1
    return entry.title, wc

# apcounts = {}
# wordcounts = {}
# feedlist = []
# for feedurl in file('feedlist.txt'):
#     feedlist.append(feedurl)
#     feed = feedparser.parse(feedurl)
#     try:
#         blog_title = feed.feed.title
#     except:
#         blog_title = "No Title"
#     for entry in feed.entries:
#         entry_title, wc = get_word_counts(entry)
#         wordcounts[blog_title + " - " + entry_title] = wc
#         for word, count in wc.items():
#             apcounts.setdefault(word, 0)
#             if count >= 1:
#                 apcounts[word] += 1

# wordlist = []
# for w, bc in apcounts.items():
#     frac = float(bc) / len(feedlist)
#     if 0.1 < frac < 0.5:
#         wordlist.append(w)

# out = file("entrydata.txt", "w")
# out.write("entry")
# for word in wordlist:
#     out.write("\t%s" % word)
# out.write("\n")
# for blog, wc in wordcounts.items():
#     # deal with unicode
#     blog = blog.encode('ascii', 'ignore')
#     out.write(blog)
#     for word in wordlist:
#         if word in wc:
#             out.write('\t%d' % wc[word])
#         else:
#             out.write('\t0')
#     out.write("\n")

import clusters
def __main__():
    entries, words, data = clusters.read_file('entrydata.txt')
    clust = clusters.hcluster(data)
    clusters.draw_dendogram(clust, entries, jpeg="ex2dend.jpg")
