"""
Arbitrary Phrase Length

This chapter showed you how to extract word pairs as well as individual words.
Make the feature extraction configurable to extract up to a specified number 
of words as a single feature.
"""
import re

def extract_n_groups(doc, n):
    splitter = re.compile("\\W*")
    words = [s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]
    pairs = []
    for i in range(len(words) - n):
        pairs.append(words[i:i+n])
    return pairs



