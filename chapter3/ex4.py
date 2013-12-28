"""
Exercise 4

Find out what Manhattan distance is. Create a function for it and see how it changes the results
 for the Zebo dataset.
"""
import clusters

def minus(x, y):
    return x - y

def manhattan_distance(v1, v2):
    return sum(map(abs, map(minus, v1, v2)))


def __main__():
    wants, people, data = clusters.read_file('zebo.txt')
    clust = clusters.hcluster(data, distance=manhattan_distance)
    clusters.draw_dendogram(clust, wants, jpeg="ex4dend.jpg")

# The clustering got even worse. If the clustering method doesn't make sense things don't work very well it seems.

