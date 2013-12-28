"""
Exercise 7

Multidemensional scaling in two dimensions is easy to print, but scaling can be
done in any number of dimensions. Try changing the code to scale to two dimensions.
Now try making it work for all dimensions.
"""

def scale_down(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distance bettween every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    loc = [[random.random(), random.random()] for i in range(n)]
    # loc = [[random.random()] for i in range(n)]
    # loc = [[random.random(), random.random(), random.random()] for i in range(n)]


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
                if j == k: continue
                if realdist[j][k] == 0: continue
                error_term = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                # Each point needs to be moved away from or towards te other point
                # in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * error_term
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * error_term

                totalerror += abs(error_term)
        print totalerror
        # If the answer got worse by moving the points we are done.
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    return loc