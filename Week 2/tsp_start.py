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
    all_cities = list(cities.copy())
    route = [all_cities.pop(0)]
    while len(all_cities) > 0:
        nearest = [route[0],9999999]
        for x in all_cities:
            dist = distance(route[-1], x)
            if dist < nearest[1]:
                nearest = [x, dist]
        route.append(nearest[0])
        all_cities.remove(nearest[0])
        route = removeIntersectByCity(route, route[-2])
    for index, city1 in enumerate(route):
        route = removeIntersectByCity(route, city1)
    return route

def removeIntersectByCity(route, city):
    cityindex = route.index(city)
    for index, city3 in enumerate(route):
        if index != cityindex:
            if cityindex == len(route)-1:
                index2 = 0
                city2 = route[0]
            else:
                index2 = cityindex + 1
                city2 = route[index2]
            if index == len(route)-1:
                index4 = 0
                city4 = route[0]
            else:
                index4 = index+1
                city4 = route[index4]
            if city != city4 and city != city3:
                if intersection_is_valid(city, city2, city3, city4):
                    switching1 = city2
                    switching2 = city3
                    route[index2] = switching2
                    route[index] = switching1
    return route

#def removeIntersects(route, last=()):
    intersecting = False
    if len(route) >= 4:
        for index, city1 in enumerate(route):
            if index == len(route)-1:
                index2 = 0
                city2 = route[0]
            else:
                index2 = index + 1
                city2 = route[index2]
            for index3, city3 in enumerate(route):
                if index3 == len(route)-1:
                    index4 = 0
                    city4 = route[0]
                else:
                    index4 = index3+1
                    city4 = route[index4]
                if last != city1 and city1 != city4 and city1 != city3:
                    if intersection_is_valid(city1, city2, city3, city4):
                        switching1 = city2
                        switching2 = city3
                        route[index2] = switching2
                        route[index3] = switching1
                        intersecting = True
    return route, intersecting

def calculate_slope(a, b):
    if b.x-a.x == 0:
        return b.x
    else:
        return (b.y - a.y)/(b.x-a.x)
        
def calculate_x_intersect(a,b,c,d):
    slope_ab = calculate_slope(a, b)
    slope_cd = calculate_slope(c, d)
    base_ab = (a.y - (slope_ab * a.x))
    base_cd = (c.y - (slope_cd * c.x))
    slope_diff = slope_cd - slope_ab
    x = (base_ab - base_cd) / slope_diff
    return x

def calculate_y_intersect(a,b,c,d):
    y = calculate_slope(a, b) * calculate_x_intersect(a, b, c, d) + (a.y - (calculate_slope(a,b)* a.x))
    
    return y

def intersection_is_valid(a,b,c,d):
    if calculate_slope(c, d) - calculate_slope(a,b) == 0:
        return False
    x = calculate_x_intersect(a,b,c,d)
    y = calculate_y_intersect(a,b,c,d)
    if min([a.x,b.x]) < x < max([a.x,b.x]) and min([a.y,b.y]) < y < max([a.y,b.y]):
        if min([c.x,d.x]) < x < max([c.x,d.x]) and min([c.y,d.y]) < y < max([c.y,d.y]):
            return True
        else: return False
    else:
        return False


# give a demo with 10 cities using brute force
#plot_tsp(try_all_tours, make_cities(10))
# opdracht a:
# 10 city tour with length 3062.4 in 0.000 secs for nearest_neighbor
#10 city tour with length 2305.8 in 1.766 secs for try_all_tours
#opdracht b: 500 city tour with length 22253.4 in 0.047 secs for nearest_neighbor
generated = make_cities(20)
plot_tsp(nearest_neighbor, generated)
# complexiteit 2-opt: O = n^3
plot_tsp(nearest_neighbor_w_intersect, generated)