"""Modify the K-means clustering function to return, along with
the cluster results, the total distance between all the items
and their respective centroids.
"""


def k_cluster(rows, distance=pearson, k=4):
    # Determine the min and max vaulues for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
              for i in range(len(rows[0]))]

    # create k centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))]
                for j in range(k)]

    last_matches = None
    for t in range(15):
        print('Iteration %d' % t)
        best_matches = [[] for i in range(k)]

        # Find what centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row):
                    best_match = i
            best_matches[best_match].append(j)

        # If the results are tthe same as last time, this is complete.
        if best_matches == last_matches:
            break

        last_matches = best_matches

        # Move the centroids to the average of their members.
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for rowid in best_matches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs

    # Exercise 5
    total_error = 0
    for i in range(k):
        for match in best_matches[i]:
            total_error += distance(clusters[i], rows[match])
    return total_error, best_matches