"""
Exercise 2

Annealing Starting Points

The outcome of simulated annealing depends heavily on the starting point.
Build a new optimization that does simulated annealing from multiple starting
solutions and returns the best one.
"""
import optimization

def restart_annealing(num_tries, domain, cost_fn, t=10000.0, cool=0.95, step=1):
    assert(num_tries > 0)
    solutions = [] 
    for i in range(num_tries):
        solutions.append(optimization.annealing_optimize(domain, cost_fn, t, cool, step))

    ranked_solutions = [(cost_fn(sol), sol) for sol in solutions]
    ranked_solutions.sort()
    return ranked_solutions[0][1]


