"""
Exercise 3

Try using actual (Euclidean) distance for blog clustering. How does this change the result?
"""
import clusters
from math import sqrt

def square(x):
    return x * x

def minus(x, y):
    return x - y

def euclidean_distance(v1, v2):
	return sqrt(sum(map(square, map(minus, v1, v2))))

def __main__():
    blognames, words, data = clusters.read_file("blogdata.txt")
    clust = clusters.hcluster(data, distance=euclidean_distance)
    clusters.draw_dendogram(clust, blognames, jpeg="ex3dendrogram.jpg")

# I think this weights against groupings that have similar word use rates but different word use counts.