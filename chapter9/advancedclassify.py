class MatchRow:
    def __init__(self, row, all_numbers=False):
        if all_numbers:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[:len(row)-1]
        self.match = int(row[len(row) - 1])

def load_match(f, all_numbers=False):
    rows = []
    for line in file(f):
        rows.append(MatchRow(line.split(","), all_numbers))
    return rows

ages_only = load_match("agesonly.csv", all_numbers=True)
match_maker = load_match("matchmaker.csv")

from pylab import *

def plot_age_matches(rows):
    xdm =  [r.data[0] for r in rows if r.match == 1]
    ydm =  [r.data[1] for r in rows if r.match == 1]

    xdn = [r.data[0] for r in rows if r.match == 0]
    ydn = [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, "go")
    plot(xdn, ydn, "ro")

    show()

# plot_age_matches(ages_only)


def linear_train(rows):
    averages = {}
    counts = {}
    for row in rows:
        cl = row.match
        averages.setdefault(cl, [0.0] * (len(row.data)))
        counts.setdefault(cl, 0)

        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])
        counts[cl] += 1

    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]
    return averages

def dotproduct(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))


def dp_classify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    return 0 if y > 0 else 1


def yesno(v):
    return 1 if v == "yes" else -1


def match_count(interests1, interests2):
    l1 = interests1.split(":")
    l2 = interests2.split(":")

    x = 0
    for interest in l1:
        if interest in l2:
            x += 1
    return x


def get_mile_distance(v):
    """
    Too lazy to fill this out.
    """
    return 0

    
