from math import sqrt
from operator import mul
from PIL import Image, ImageDraw
import random


def read_file(file_name):
    """
    Accepts a tab seperated file containing a table w/ row and column names.

    Returns a tuple row_names, col_names, data.
    """
    lines = [line for line in file(file_name)]

    # first line is column titles
    col_names = lines[0].strip().split('\t')[1:]
    row_names = []
    data = []
    for line in lines[1:]:
        row = line.strip().split('\t')

        # First column in each row is the row name
        row_names.append(row[0])
        data.append(map(float, row[1:]))
    return row_names, col_names, data


def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1_sq = sum([pow(v, 2) for v in v1])
    sum2_sq = sum([pow(v, 2) for v in v2])
    pSum = sum(map(mul, v1, v2))

    # Calculuate r (Pearson score)
    num = pSum - ((sum1 * sum2) / len(v1))
    den = sqrt((sum1_sq - pow(sum1, 2) / len(v1)) * (sum2_sq - pow(sum2, 2) / len(v1)))

    return 1 - num / den if den else 0


class BiCluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

    def get_height(self):
        if self.left is None and self.right is None:
            return 1
        else:
            return self.left.get_height() + self.right.get_height()

    def get_depth(self):
        if self.left is None and self.right is None:
            return 0
        return max(self.left.get_depth(), self.right.get_depth()) + self.distance


def draw_node(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = clust.left.get_height() * 20
        h2 = clust.right.get_height() * 20
        top = y - (h1+h2) / 2
        bottom = y + (h1 + h2) / 2

        line_length = clust.distance * scaling

        # Vertical line from this cluster to children
        draw.line((x, top + h1/2, x, bottom-h2/2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top + h1/2, x + line_length, top+h1/2), fill=(255, 0, 0))

        #Horiztonal line to right item
        draw.line((x, bottom-h2/2, x + line_length, bottom-h2/2), fill=(255, 0, 0))

        draw_node(draw, clust.left, x + line_length, top+h1/2, scaling, labels)
        draw_node(draw, clust.right, x + line_length, bottom-h2/2, scaling, labels)
    else:
        draw.text((x+5, y-7), labels[clust.id], (0, 0, 0))


def draw_dendogram(clust, labels, jpeg="clusters.jpeg"):
    h = clust.get_height() * 20
    w = 1200 
    #font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", 14)

    depth = clust.get_depth()
    scaling = float(w - 150) / depth

    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))

    draw_node(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, "JPEG")


def hcluster(rows, distance=pearson):
    distances = {}
    current_cluster_id = -1

    # Clusters are initially just the rows
    clusters = [BiCluster(rows[i], id=i) for i in range(len(rows))]

    while len(clusters) > 1:
        lowest_pair = (0, 1)
        closest = distance(clusters[0].vec, clusters[1].vec)

        # loop through every pair looking for the smallest distance between clusters, w/ memoization
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if (clusters[i].id, clusters[j].id) not in distances:
                    distances[(clusters[i].id, clusters[j].id)] = distance(clusters[i].vec, clusters[j].vec)
                d = distances[(clusters[i].id, clusters[j].id)]

                if d < closest:
                    closest = d
                    lowest_pair = (i, j)
        merge_vec = [(clusters[lowest_pair[0]].vec[i] + clusters[lowest_pair[1]].vec[i]) / 2.0
                        for i in range(len(clusters[0].vec))]

        new_cluster = BiCluster(merge_vec, 
                                left=clusters[lowest_pair[0]], 
                                right=clusters[lowest_pair[1]],
                                distance=closest,
                                id=current_cluster_id)

        current_cluster_id -= 1
        del clusters[lowest_pair[1]]
        del clusters[lowest_pair[0]]
        clusters.append(new_cluster)
    return clusters[0]


def print_clust(clust, labels=None, n=0):
    for i in range(n):
        print(" ", end="")
    if clust.id < 0:
        print(" -")
    else:
        print (clust.id if not labels else labels[clust.id])
    if clust.left:
        print_clust(clust.left, labels=labels, n=n+1)
    if clust.right:
        print_clust(clust.right, labels=labels, n=n+1)


def rotate_matrix(data):
    new_data = []
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data


def __main__():
    blognames, words, data = read_file("blogdata.txt")
    err, matches = k_cluster(data, k=10)
    print([blognames[i] for i in matches[0]])
    # clust = hcluster(data)
    # draw_dendogram(clust, blognames, jpeg="blogclust.jpg")

    # rotated_data = rotate_matrix(data)
    # word_clusters = hcluster(data)
    # draw_dendogram(word_clusters, words, jpeg="wordclusters.jpg")

    # blognames, words, data = read_file("blogdata2.txt")
    # clust = hcluster(data)
    # draw_dendogram(clust, blognames, jpeg="blogclust2.jpg")

    # rotated_data = rotate_matrix(data)
    # word_clusters = hcluster(data)
    # draw_dendogram(word_clusters, words, jpeg="wordclusters2.jpg")


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


def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0
    for i in range(len(v1)):
        if v1[i] != 0: c1 += 1
        if v2[i] != 0: c2 += 1
        if v1[i] != 0 and v2[i] != 0: shr += 1

    return 1.0 - (float(shr)/(c1+c2-shr))

#wants, people, data = read_file('zebo.txt')
#clust = hcluster(data, distance=tanimoto)
#draw_dendogram(clust, wants, jpeg="wants_cluster.jpg")


def scale_down(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distance bettween every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    outer_sum = 0.0
    lasterror = None
    for m in range(1000):
        # Find projected distance
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                            for x in range(len(loc[i]))]))

        grad = [[0.0, 0.0] for i in range(n)]
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: 
                    continue
                if realdist[j][k] == 0: 
                    continue
                error_term = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                # Each point needs to be moved away from or towards te other point
                # in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * error_term
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * error_term

                totalerror += abs(error_term)
        print(totalerror)
        # If the answer got worse by moving the points we are done.
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    return loc


def draw2d(data, labels, jpeg="mds2d.jpg"):
    img = Image.new("RGB", (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.6) * 1000
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, "JPEG")

#blognames, words, data = read_file("blogdata.txt")
#coords = scale_down(data)
#draw2d(coords, blognames, jpeg="blog2d.jpg")
