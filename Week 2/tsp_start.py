import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

def nearest_neighbor(cities):
    all_cities = list(cities)
    route = [all_cities.pop(0)]
    while len(all_cities) > 0:
        nearest = [route[0],9999999]
        for x in all_cities:
            dist = distance(route[-1], x)
            if dist < nearest[1]:
                nearest = [x, dist]
        route.append(nearest[0])
        all_cities.remove(nearest[0])
    return route

def nearest_neighbor_w_intersect(cities):    
    all_cities = list(cities)
    route = [all_cities.pop(0)]
    while len(all_cities) > 0:
        nearest = [route[0],9999999]
        for x in all_cities:
            dist = distance(route[-1], x)
            if dist < nearest[1]:
                nearest = [x, dist]
        route.append(nearest[0])
        all_cities.remove(nearest[0])
        route = removeIntersects(route)
    return route

def removeIntersects(route):
    intersecting = 0
    for index, y in enumerate(route):
        if(index < len(route) - 3):
            if doIntersect(y, route[index + 1], route[-2], route[-1]):
                print("intersecting1111", route[index], route[index+1], route[-2], route[-1])
                route[index+1], route[-2] = route[-2], route[index+1]
                print("intersecting2222", route[index], route[index+1], route[-2], route[-1])
    return route

def onSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
 
def orientation(p, q, r):
     
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0

def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
    return False

# give a demo with 10 cities using brute force
#plot_tsp(try_all_tours, make_cities(10))
# opdracht a:
# 10 city tour with length 3062.4 in 0.000 secs for nearest_neighbor
#10 city tour with length 2305.8 in 1.766 secs for try_all_tours
#opdracht b: 500 city tour with length 22253.4 in 0.047 secs for nearest_neighbor
generated = make_cities(500)
plot_tsp(nearest_neighbor, generated)
# complexiteit 2-opt: O = n^3
plot_tsp(nearest_neighbor_w_intersect, generated)