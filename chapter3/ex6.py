"""
Exercise 6

After completing exercise five, create a function that runs K-means
clustering over different values of k. How does the total distance
change as the number if clusters increases? At what point does the
improvement from having more clusters become very small?
"""
import clusters
from matplotlib import pyplot
trash, other_trash, DATA = clusters.read_file("blogdata.txt")


def run_experiment(k):
    return clusters.k_cluster(DATA, k=k)[0]


def run_experiments():
    ks = []
    errors = []
    pyplot.xlabel("K Value")
    pyplot.ylabel("Error")
    pyplot.xlim([0, 25])
    pyplot.ylim([0, 100])
    pyplot.title("Plot of K Value and Error")
    pyplot.ion()
    for i in range(2, 25):
        ks.append(i)
        errors.append(run_experiment(i))
        pyplot.plot(ks, errors, "b.")
        if i == 2:
            pyplot.show()
        pyplot.pause(3)

run_experiments()
