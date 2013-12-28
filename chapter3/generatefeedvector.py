"""
This file downloads a dataset of word counts and saves them. Note that 
after running this file some manual cleanup might be necessary.
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

def get_word_counts(url):
    """
    Returns title and dictionary of the word counts for an RSS feed.
    """
    d = feedparser.parse(url)
    wc = {}

    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        words = get_words(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    try:
        return d.feed.title, wc
    except:
        return "No Title", wc

apcounts = {}
wordcounts = {}
feedlist = []
for feedurl in file('feedlist.txt'):
    feedlist.append(feedurl)
    title, wc = get_word_counts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcounts.setdefault(word, 0)
        if count >= 1:
            apcounts[word] += 1

wordlist = []
for w, bc in apcounts.items():
    frac = float(bc) / len(feedlist)
    if 0.1 < frac < 0.5:
        wordlist.append(w)

out = file("blogdata.txt", "w")
out.write("Blog")
for word in wordlist:
    out.write("\t%s" % word)
out.write("\n")
for blog, wc in wordcounts.items():
    # deal with unicode
    blog = blog.encode('ascii', 'ignore')
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write("\n")