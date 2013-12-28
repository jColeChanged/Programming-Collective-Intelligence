"""
Exercise 1 - Word Seperation

The seperate_words method currently considers any nonalphanumberic character
to be a seperator. Write a beter seperator that indexes words like C++.
"""

def seperate_words(words):
    words = words.replace(".", "")
    words = words.replace(",", "")
    words = words.split()
    return [word.lower() for word in words]


test_cases = "C++ $20 Ph.D.           normal, words 617-555-1212."
seperate_words(test_cases)