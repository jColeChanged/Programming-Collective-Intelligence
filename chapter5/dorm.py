import random
import math
import optimization
# The dorms, each of which has two available spaces

dorms = ['Zeus','Athena','Hercules','Bacchus','Pluto']
# People, along with their first and second choices
prefs=[('Toby', ('Bacchus', 'Hercules')),
       ('Steve', ('Zeus', 'Pluto')),
       ('Andrea', ('Athena', 'Zeus')),
       ('Sarah', ('Zeus', 'Pluto')),
       ('Dave', ('Athena', 'Bacchus')),
       ('Jeff', ('Hercules', 'Pluto')),
       ('Fred', ('Pluto', 'Athena')),
       ('Suzie', ('Bacchus', 'Hercules')),
       ('Laura', ('Bacchus', 'Hercules')),
       ('Neil', ('Hercules', 'Athena'))]

# (0, 9), (0, 8), (0, 7)... (0, 1)
domain = [(0, i) for i in range(0, len(dorms) * 2)][::-1]

def print_solution(vec):
    slots = []
    # Create two slots for each dorms
    for i in range(len(dorms)):
        slots += [i, i]

    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        print prefs[i][0], dorm
        del slots[x]

def dorm_cost(vec):
    cost = 0
    # cCreate list a of slots
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

    # Loop over each student
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        if pref[0] == dorm:
            cost += 0
        elif pref[1] == dorm:
            cost += 1
        else:
            cost += 3
        del slots[x]
    return cost

# Not on the list costs 3
#dorm_cost(optimization.random_optimize(domain, dorm_cost))
#dorm_cost(optimization.genetic_optimize(domain, dorm_cost))

