from random import random, randint
import math

def wine_price(rating, age):
    peak_age = rating - 50

    # Calculate the price based on the rating
    price = rating / 2
    if age > peak_age:
        # past its peak, goes bad in five years
        price = price * (5 - (age - peak_age))
    else:
        # Increase price as it approaches its peak
        price = price * (5 * ((age + 1) / peak_age))
    if price < 0:
        price = 0
    return price


def wine_set1():
    rows = []
    for i in range(300):
        rating = random() * 50 + 50
        age = random() * 50
       
        # Get the refrence price
        price = wine_price(rating, age)

        # Add some noise
        price *= (random() * 0.4 + 0.8)
        rows.append({"input": (rating, age), "result": price})
    return rows


def wine_set2():
    rows = []
    for i in range(300):
        rating = random() * 50 + 50
        age = random() * 50
        aisle = float(randint(1, 20))
        bottlesize = [375.0, 750.0, 1500.0, 3000.0][randint(0,3)]

        # Get the refrence price
        price = wine_price(rating, age)
        price *= bottlesize/750.0
        price *= (random() * 0.9 + 0.2)

        rows.append({"input": (rating, age, aisle, bottlesize), "result": price})
    return rows


def euclidean(v1, v2):
    distance = 0
    for i in range(len(v1)):
        distance += (v1[i] - v2[i]) ** 2
    return math.sqrt(distance)


def get_distances(data, vec1):
    distance_list = []
    for i in range(len(data)):
        vec2 = data[i]['input']
        distance_list.append((euclidean(vec1, vec2), i))
    distance_list.sort()
    return distance_list

def knn_estimate(data, vec1, k=3):
    # Get sorted distances
    distance_list = get_distances(data, vec1)
    
    avg = 0
    for i in range(k):
        index = distance_list[i][1]
        avg += data[index]['result']
    avg = avg / k
    return avg


def inverse_weight(dist, num=1.0, const=0.1):
    return num / (dist + const)


def subtract_weight(dist, const=1.0):
    if dist > const:
        return 0
    else:
        return const - dist


def gaussian_weight(dist, sigma=10.0):
    return math.e ** (-dist ** 2 / (2 * sigma ** 2))


def weighted_knn(data, vec1, k=5, weightf=gaussian_weight):
    # Get sorted distances
    distance_list = get_distances(data, vec1)
    avg = 0
    total_weight = 0.0

    for i in range(k):
        distance = distance_list[i][0]
        weight = weightf(distance)
        index = distance_list[i][1]
        avg += weight * data[index]['result']
        total_weight += weight
    avg = avg / total_weight
    return avg


def divide_data(data, test=0.05):
    train_set = []
    test_set = []
    for row in data:
        if random() < test:
            test_set.append(row)
        else:
            train_set.append(row)
    return train_set, test_set

def test_algorithm(algf, trainset, testset):
    error = 0.0
    for row in testset:
        guess = algf(trainset, row["input"])
        error += (row["result"] - guess) ** 2
    return error / len(testset)

def crossvalidate(algf, data, trials=100, test=0.05):
    error = 0.0
    for i in range(trials):
        trainset, testset = divide_data(data, test)
        error += test_algorithm(algf, trainset, testset)
    return error/trials

def rescale(data, scale):
    scaled_data = []
    for row in data:
        scaled = [scale[i] * row["input"][i] for i in range(len(scale))]
        scaled_data.append({"input": scaled, "result": row["result"]})
    return scaled_data