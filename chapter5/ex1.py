"""
Exercise 1

Group travel cost function.

Add total flight time as a cost equal to $0.50 per minute on the plane.
Next try adding a penalty of $20 for making anyone get to the airport
before 8 a.m.
"""

def schedule_cost(solution):
    total_price = 0
    latest_arrival = 0
    earliest_departure = 24 * 60
    time_in_air = 0
    time_penalty = 0

    for i in range(0, len(solution), 2):
        # Get the inbound and outbound flights
        origin = PEOPLE[i/2][1]
        outbound = FLIGHTS[(origin, DESTINATION)][solution[i]]
        inbound = FLIGHTS[(DESTINATION, origin)][solution[i+1]]
        time_in_air += get_minutes(outbound[1]) - get_minutes(outbound[0])
        time_in_air += get_minutes(inbound[1]) - get_minutes(inbound[0])



        total_price += outbound[2]
        total_price += inbound[2]

        if latest_arrival < get_minutes(outbound[1]):
            latest_arrival = get_minutes(outbound[1])

        if earliest_departure > get_minutes(inbound[0]):
            earliest_departure = get_minutes(inbound[0])

    if earliest_departure < 8 * 60:
        time_pentalty = 20
    # Every person must wait at the airport until the latest person
    # arrives. They must also arrive at the same time and wait for
    # their flights.
    total_wait = 0
    for i in range(0, len(solution), 2):
        # Get the inbound and outbound flights
        origin = PEOPLE[i/2][1]
        outbound = FLIGHTS[(origin, DESTINATION)][solution[i]]
        inbound = FLIGHTS[(DESTINATION, origin)][solution[i+1]]

        total_wait += latest_arrival - get_minutes(outbound[1])
        total_wait += get_minutes(inbound[0]) - earliest_departure

    if latest_arrival < earliest_departure:
        total_price += 50
    return total_price + total_wait + time_in_air * .5 + time_penalty